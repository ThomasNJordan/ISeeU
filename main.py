import argparse, queue, sys, time, datetime as dt, pyshark
from config       import SAMPLE_DURATION
from capture      import CSICapture
from csi_parser   import aoa_from_pkt
from cir_distance import cir_distance
from pointcloud   import pol_to_cart
from export_udp   import UDPCSVSender

# ---------------------------------------------------------------------------

def run_live(iface, seconds, sender):
    q = queue.Queue()
    cap = CSICapture(q, iface)
    cap.start()
    _collect(q, seconds, sender)
    cap.stop()

def run_stdin(sender):
    q = queue.Queue()
    pkts = pyshark.FileCapture(stdin=True, keep_packets=False, use_json=True)
    for p in pkts:
        q.put(p.get_raw_packet())
    _collect(q, None, sender)

# ---------------------------------------------------------------------------

def _collect(q, seconds, sender):
    t0 = time.time()
    while seconds is None or time.time() - t0 < seconds:
        try:
            pkt = q.get(timeout=1)
        except queue.Empty:
            continue

        res = aoa_from_pkt(pkt)          # (angle_deg, csi_mat) or None
        if res is None:
            continue
        theta, csi = res

        dist = cir_distance(csi)
        if dist is None:
            continue

        x, y, _ = pol_to_cart(dist, theta)
        timestamp = dt.datetime.utcnow().isoformat(timespec="milliseconds")
        sender.send([timestamp, f"{dist:.3f}", f"{theta:.1f}",
                     f"{x:.3f}", f"{y:.3f}"])

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iface", help="monitor-mode interface (e.g. wlan0mon)")
    ap.add_argument("--stdin", action="store_true",
                    help="read PCAP stream from stdin instead of live iface")
    ap.add_argument("--seconds", type=int, default=SAMPLE_DURATION)
    ap.add_argument("--udp-ip",   default="127.0.0.1")
    ap.add_argument("--udp-port", type=int, default=5500)
    args = ap.parse_args()

    sender = UDPCSVSender(args.udp_ip, args.udp_port)

    try:
        if args.stdin:
            run_stdin(sender)
        elif args.iface:
            run_live(args.iface, args.seconds, sender)
        else:
            print("Use --iface <iface> OR --stdin", file=sys.stderr)
    finally:
        sender.close()
