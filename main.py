import argparse, queue, sys, time, pyshark
from config       import SAMPLE_DURATION
from capture      import CSICapture
from csi_parser   import aoa_from_pkt
from cir_distance import cir_distance
from pointcloud   import build_cloud
from visualize    import show_pointcloud

def run_live(iface, seconds):
    q = queue.Queue()
    cap = CSICapture(q, iface)
    cap.start()
    collect(q, seconds)
    cap.stop()

def run_stdin():
    q = queue.Queue()
    pkts = pyshark.FileCapture(stdin=True, keep_packets=False, use_json=True)
    for p in pkts:
        q.put(p.get_raw_packet())
    collect(q, None)

def collect(q, seconds):
    t0 = time.time()
    ds, as_ = [], []
    while seconds is None or time.time() - t0 < seconds:
        try:
            pkt = q.get(timeout=1)
        except queue.Empty:
            continue
        res = aoa_from_pkt(pkt)
        if res is None:
            continue
        ang, csi = res
        dist = cir_distance(csi)
        if dist is None:
            continue
        ds.append(dist)
        as_.append(ang)
    cloud = build_cloud(ds, as_)
    print(f"Points: {len(cloud)}")
    show_pointcloud(cloud)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iface", help="monitor-mode interface (e.g. wlan0mon)")
    ap.add_argument("--stdin", action="store_true",
                    help="read pcap stream from stdin instead of live iface")
    ap.add_argument("--seconds", type=int, default=SAMPLE_DURATION)
    args = ap.parse_args()

    if args.stdin:
        run_stdin()
    elif args.iface:
        run_live(args.iface, args.seconds)
    else:
        print("Use --iface <iface> OR --stdin", file=sys.stderr)
