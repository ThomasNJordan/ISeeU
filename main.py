"""
Live or streamed demo that prints:
    AoA  (degrees)   and   Range  (metres)
for every 802.11 packet that contains CSI.

Usage examples
--------------
# 1. Sniff with a local NIC already in monitor mode
sudo airmon-ng start wlan0          # → wlan0mon
python main.py --iface wlan0mon

# 2. Read a PCAP stream from stdin (e.g. coming over netcat)
tcpdump -i wlan0 -I -s 4096 -U -w - | nc … | python main.py
"""
import argparse, sys, queue, time, numpy as np, pyshark
from scapy.all import sniff, RadioTap

from config import (CENTER_FREQUENCY, ANTENNA_SPACING,
                    CHANNEL_BW, SPEED_OF_LIGHT)
from csi_fallback import parse_csi

# ───────────────────────────── DSP helpers ──────────────────────────────────
def aoa_bartlett(csi, d=ANTENNA_SPACING, f=CENTER_FREQUENCY):
    """
    Classical Bartlett beam-former:
      • Assume Uniform Linear Array with spacing `d`
      • Sweep −90° … +90° in 1° steps
      • Return the angle whose steering vector maximises output power

    Parameters
    ----------
    csi : ndarray  (subcarriers, N_rx)
    d   : float    antenna spacing (m)
    f   : float    carrier frequency (Hz)

    Returns
    -------
    float or None : AoA in degrees, or None if <2 RX chains.
    """
    if csi.shape[1] < 2:               # need phase diff between chains
        return None
    lamb = 3e8 / f
    thetas = np.linspace(-90, 90, 181)
    power = []
    for th in thetas:
        steering = np.exp(
            -1j * 2 * np.pi * d * np.sin(np.deg2rad(th)) / lamb
            * np.arange(csi.shape[1])
        )
        power.append(np.abs((csi @ steering.conj().T)**2).sum())
    return float(thetas[int(np.argmax(power))])

def range_from_cir(csi, bw=CHANNEL_BW):
    """
    Coarse ranging via Channel Impulse Response (IFFT of averaged CSI).

    Steps
    -----
    1. Average across RX chains → 1-D frequency response H(f)
    2. IFFT → h(τ)   (power vs. delay)
    3. Pick first significant peak index → delay_bin * (1/BW)
    4. Convert delay to distance (round-trip / 2)

    Caveat: resolution = 1/BW (25 ns ≈ 7.5 m for 40 MHz).  Good enough for
    *demo* but not sub-metre accuracy.
    """
    h = np.fft.ifft(csi.mean(axis=1))
    idx = np.argmax(np.abs(h))         # first path peak
    delay = idx / bw                   # seconds
    return 0.5 * SPEED_OF_LIGHT * delay

# ───────────────────────────── Capture back-ends ────────────────────────────
def pkt_iter_live(iface):
    """
    Generator yielding scapy packets from a live monitor-mode interface.
    """
    q = queue.Queue()
    sniff(iface=iface, store=False, prn=q.put,   # every pkt → queue
          stop_filter=lambda *_: False,          # run until Ctrl-C
          monitor=True)                          # ensure Radiotap
    while True:
        yield q.get()

def pkt_iter_stdin():
    """
    Generator yielding scapy packets read from stdin PCAP stream via pyshark.
    """
    cap = pyshark.FileCapture(stdin=True, keep_packets=False, use_json=True)
    for p in cap:
        yield p.get_raw_packet()

# ───────────────────────────── Main processing loop ─────────────────────────
def process(pkt_iter):
    """
    Consume packets, compute AoA + distance if CSI present, print result.
    """
    for pkt in pkt_iter:
        if not pkt.haslayer(RadioTap):
            continue

        csi = parse_csi(pkt)
        if csi is None:
            continue                   # not a CSI-carrying frame

        theta = aoa_bartlett(csi)
        dist  = range_from_cir(csi)

        if theta is None or dist is None:
            continue
        # Pretty-print, overwrite same line to keep console clean
        print(f"AoA: {theta:+6.1f}°,  Range: {dist:6.2f} m", end="\r",
              flush=True)

# ────────────────────────────── CLI entry point ─────────────────────────────
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iface", help="monitor-mode interface (e.g. wlan0mon)")
    args = ap.parse_args()

    try:
        if args.iface:
            print("⟲ Live sniffing …  Ctrl-C to stop")
            process(pkt_iter_live(args.iface))
        else:
            print("⟲ Reading packets from stdin …")
            process(pkt_iter_stdin())
    except KeyboardInterrupt:
        print("\nDone.")
        sys.exit(0)
