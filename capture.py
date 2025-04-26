from scapy.all import sniff, RadioTap
import queue, threading

class CSICapture:
    """
    Capture raw 802.11 frames (radiotap) from stdin or an interface
    and push them into a thread-safe queue.
    """
    def __init__(self, frame_q: queue.Queue, iface: str | None = None):
        self.iface  = iface
        self.q      = frame_q
        self._stop  = threading.Event()

    def _cb(self, pkt):
        if pkt.haslayer(RadioTap):
            self.q.put(pkt)

    def start(self):
        if self.iface is None:           # reading from stdin via pyshark
            raise RuntimeError("Iface is None – use pyshark for stdin mode")
        t = threading.Thread(target=lambda:
            sniff(iface=self.iface,
                  prn=self._cb,
                  store=False,
                  stop_filter=lambda *_: self._stop.is_set()))
        t.daemon = True
        t.start()

    def stop(self):
        self._stop.set()
