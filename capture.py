from scapy.all import sniff, RadioTap
from CSIKit.tools import read_pcap
import queue, threading, time

class CSICapture:
    """
    Capture CSI and raw 802.11 frames in monitor mode.
    Writes frames to a thread-safe queue for downstream processing.
    """

    def __init__(self, iface: str, frame_queue: queue.Queue):
        self.iface = iface
        self.q     = frame_queue
        self._stop = threading.Event()

    def _callback(self, pkt):
        if not pkt.haslayer(RadioTap):       # basic guard
            return
        self.q.put(pkt)

    def start(self):
        t = threading.Thread(target=lambda:
            sniff(iface=self.iface,
                  prn=self._callback,
                  store=False,
                  stop_filter=lambda _: self._stop.is_set()))
        t.daemon = True
        t.start()

    def stop(self):
        self._stop.set()
