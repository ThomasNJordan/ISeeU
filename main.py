"""
AoA + range estimation from a pcap file produced by **airodump-ng**.

Usage
-----
# 1. Live pcap tail (router or same PC)
airodump-ng wlan0mon --output-format pcap --write /tmp/csi_capture

# 2. Run this script on the pcap file
python main.py --pcap /tmp/csi_capture-01.cap

# Optional: still supports --iface <wlan0mon> for live sniff
"""
from __future__ import annotations
import argparse, sys, queue, numpy as np, pyshark, pathlib, time
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
    num_rx = csi_matrix.shape[1]
    if num_rx < 2:
        return None
    wavelength_m      = 3e8 / carrier_freq_hz
    angle_grid_deg    = np.linspace(-90, 90, 181)      # 1° steps
    power_along_grid  = []
    for angle_deg in angle_grid_deg:
        steering_vec = np.exp(
            -1j * 2 * np.pi * antenna_spacing_m
            * np.sin(np.deg2rad(angle_deg)) / wavelength_m
            * np.arange(num_rx)
        )
        projected_power = np.abs((csi_matrix @ steering_vec.conj().T) ** 2).sum()
        power_along_grid.append(projected_power)
    return float(angle_grid_deg[int(np.argmax(power_along_grid))])

def estimate_distance(csi_matrix: np.ndarray,
                      channel_bw_hz: float = CHANNEL_BW) -> float:
    freq_response     = csi_matrix.mean(axis=1)
    impulse_response  = np.fft.ifft(freq_response)
    first_path_index  = int(np.argmax(np.abs(impulse_response)))
    delay_seconds     = first_path_index / channel_bw_hz
    return 0.5 * SPEED_OF_LIGHT * delay_seconds

# ── Packet generators ───────────────────────────────────────────────────────
def generate_packets_live(interface_name: str):
    """
    Yield scapy packets from a live monitor-mode interface.
    """
    packet_queue: queue.Queue = queue.Queue()

    sniff(iface=interface_name,
          store=False,
          monitor=True,
          prn=packet_queue.put,
          stop_filter=lambda *_: False)
    while True:
        yield packet_queue.get()

def generate_packets_pcap(pcap_path: pathlib.Path):
    """
    Yield packets as they are appended to <pcap_path>.
    pyshark with follow=True keeps the file open and
    delivers new frames almost instantly.
    """
    capture = pyshark.FileCapture(
        str(pcap_path),
        keep_packets=False,
        follow=True,            # <- tail -F
        use_json=True
    )
    for pkt in capture:
        yield pkt.get_raw_packet()

# ── Core processing loop ────────────────────────────────────────────────────
def process(packet_iterator):
    """
    Consume packets, compute AoA & distance if CSI present, print results.
    """
    for packet in packet_iterator:
        if not packet.haslayer(RadioTap):
            continue
        csi_matrix = parse_csi(packet)
        if csi_matrix is None:
            continue
        angle_deg   = estimate_aoa(csi_matrix)
        distance_m  = estimate_distance(csi_matrix)
        if angle_deg is None:
            continue
        print(f"AoA {angle_deg:+6.1f}°   Range {distance_m:6.2f} m",
              end="\r", flush=True)

# ── CLI entry point ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--pcap",  type=pathlib.Path,
                     help="Path to airodump-ng .cap file (tail in real-time)")
    cli.add_argument("--iface",
                     help="Alternative: live monitor-mode interface name")
    args = cli.parse_args()

    try:
        if args.pcap:
            if not args.pcap.exists():
                print("Waiting for pcap file to appear …")
                while not args.pcap.exists():
                    time.sleep(0.5)
            print(f"⟲ Tailing {args.pcap}  (Ctrl-C to stop)")
            process(generate_packets_pcap(args.pcap))
        elif args.iface:
            print("⟲ Live sniffing interface …  Ctrl-C to stop")
            process(generate_packets_live(args.iface))
        else:
            cli.error("Provide either --pcap <file> or --iface <intf>")
    except KeyboardInterrupt:
        print("\nStopped by user.")
        sys.exit(0)
