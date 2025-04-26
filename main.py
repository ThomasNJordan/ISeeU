"""
Compute AoA + distance from a pcap that airodump-ng is writing,
and append each result as a JSON object to <output.json>.

Run:
    # 1) Capture on router or PC
    airodump-ng wlan0mon --output-format pcap --write /tmp/csi_capture

    # 2) Analyse on the same or another PC
    python main.py --pcap /tmp/csi_capture-01.cap --json aoa_range.json
"""
from __future__ import annotations
import argparse, sys, queue, time, json, datetime as dt, pathlib, numpy as np
import pyshark
from scapy.all import sniff, RadioTap

from config import (
    CENTER_FREQUENCY,
    ANTENNA_SPACING,
    CHANNEL_BW,
    SPEED_OF_LIGHT,
)
from csi_fallback import parse_csi

# ── DSP helpers (unchanged) ─────────────────────────────────────────────────
def estimate_aoa(csi_matrix: np.ndarray,
                 antenna_spacing_m: float = ANTENNA_SPACING,
                 carrier_freq_hz: float = CENTER_FREQUENCY) -> float | None:
    """Bartlett beam-forming scan (−90°..+90° in 1° steps)."""
    num_rx = csi_matrix.shape[1]
    if num_rx < 2:
        return None
    wavelength_m      = 3e8 / carrier_freq_hz
    angles_deg        = np.linspace(-90, 90, 181)
    powers            = []
    for angle in angles_deg:
        steering = np.exp(
            -1j * 2 * np.pi * antenna_spacing_m
            * np.sin(np.deg2rad(angle)) / wavelength_m
            * np.arange(num_rx)
        )
        powers.append(np.abs((csi_matrix @ steering.conj().T) ** 2).sum())
    return float(angles_deg[int(np.argmax(powers))])

def estimate_distance(csi_matrix: np.ndarray,
                      channel_bw_hz: float = CHANNEL_BW) -> float:
    """First peak of CIR → coarse propagation delay → distance."""
    freq_response    = csi_matrix.mean(axis=1)
    impulse_response = np.fft.ifft(freq_response)
    first_peak_idx   = int(np.argmax(np.abs(impulse_response)))
    delay_s          = first_peak_idx / channel_bw_hz
    return 0.5 * SPEED_OF_LIGHT * delay_s

# ── Packet generators ───────────────────────────────────────────────────────
def packets_from_pcap_live(pcap_path: pathlib.Path):
    """
    Tail a growing pcap file (airodump-ng) and yield scapy packets as they land.
    """
    capture = pyshark.FileCapture(
        str(pcap_path), keep_packets=False, follow=True, use_json=True
    )
    for pkt in capture:
        yield pkt.get_raw_packet()

def packets_from_interface(interface_name: str):
    """Fallback: yield packets from a live monitor-mode NIC on this PC."""
    pkt_queue: queue.Queue = queue.Queue()
    sniff(iface=interface_name,
          store=False, monitor=True, prn=pkt_queue.put,
          stop_filter=lambda *_: False)
    while True:
        yield pkt_queue.get()

# ── Core processing loop ────────────────────────────────────────────────────
def analyse(packet_iterator, json_path: pathlib.Path):
    """
    Compute AoA + distance for every CSI packet and append it to <json_path>.
    """
    with json_path.open("a", encoding="utf-8") as json_file:   # append mode
        for packet in packet_iterator:
            if not packet.haslayer(RadioTap):
                continue
            csi_matrix = parse_csi(packet)
            if csi_matrix is None:
                continue
            angle_deg   = estimate_aoa(csi_matrix)
            distance_m  = estimate_distance(csi_matrix)
            if angle_deg is None:
                continue   # single-antenna packets, etc.

            record = {
                "timestamp"  : dt.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
                "angle_deg"  : round(angle_deg, 1),
                "distance_m" : round(distance_m, 3)
            }
            json_file.write(json.dumps(record) + "\n")
            json_file.flush()            # ensure real-time updates

# ── CLI entry point ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--pcap",  type=pathlib.Path,
                     help="Path to airodump-ng .cap file (tailed live)")
    cli.add_argument("--iface",
                     help="Alternative: live monitor-mode interface")
    cli.add_argument("--json",  type=pathlib.Path, default="aoa_range.json",
                     help="Output NDJSON file (default: aoa_range.json)")
    args = cli.parse_args()

    try:
        if args.pcap:
            if not args.pcap.exists():
                print("Waiting for pcap file to appear …")
                while not args.pcap.exists():
                    time.sleep(0.5)
            print(f"⟲ Tailing {args.pcap}  →  {args.json}   Ctrl-C to stop")
            analyse(packets_from_pcap_live(args.pcap), args.json)
        elif args.iface:
            print(f"⟲ Live sniff {args.iface}  →  {args.json}   Ctrl-C to stop")
            analyse(packets_from_interface(args.iface), args.json)
        else:
            cli.error("Provide either --pcap <file> or --iface <intf>")
    except KeyboardInterrupt:
        print("\nStopped by user.")
        sys.exit(0)
