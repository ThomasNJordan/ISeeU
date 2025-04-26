import socket, csv, io

class UDPCSVSender:
    """Send one CSV row per UDP datagram."""
    def __init__(self, dest_ip="127.0.0.1", dest_port=5500):
        self.addr = (dest_ip, dest_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._buf  = io.StringIO()
        self._csv  = csv.writer(self._buf)

    def send(self, row_iterable):
        self._buf.seek(0); self._buf.truncate(0)
        self._csv.writerow(row_iterable)
        self.sock.sendto(self._buf.getvalue().encode(), self.addr)

    def close(self):
        self.sock.close()
