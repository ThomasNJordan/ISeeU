import argparse, queue, time
from config       import SAMPLE_DURATION
from capture      import CSICapture
from inject       import send_ftm_burst
from rtt          import ftm_distance
from csi_parser   import aoa_from_csi
from pointcloud   import build_pointcloud
from visualize    import show_pointcloud

def run(iface: str, seconds: int):
    q = queue.Queue(maxsize=4096)
    cap = CSICapture(iface, q)
    cap.start()

    start = time.time()
    distances, angles = [], []

    try:
        while time.time() - start < seconds:
            # --- Active measurement burst every 0.5 s
            send_ftm_burst(iface)

            # --- Wait for a matching FTM response + CSI sample
            pkt = q.get(timeout=2)
            if pkt.type == 0 and pkt.subtype == 13:      # action frame
                # (Illustrative!) your driver may expose nanosec timestamps as pkt.time_ns
                t1, t2, t3, t4 = pkt.time_ns, pkt.time_ns+10, pkt.time_ns+20, pkt.time_ns+30
                d = ftm_distance(t1, t2, t3, t4)
                distances.append(d)

            if hasattr(pkt, "csi"):                      # driver-specific attr
                theta = aoa_from_csi(pkt.csi)
                angles.append(theta)

    finally:
        cap.stop()

    cloud = build_pointcloud(distances, angles)
    print(f"[+] Collected {cloud.shape[0]} points")
    show_pointcloud(cloud)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iface",   required=True, help="monitor-mode interface (e.g. wlan0mon)")
    ap.add_argument("--seconds", type=int, default=SAMPLE_DURATION)
    run(**vars(ap.parse_args()))
