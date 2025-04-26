"""
Minimal CSI parsers for:
  • ath9k  (Atheros CSI Tool / OpenWrt patch)   – AR9580
  • Intel 5300
  • Nexmon (Broadcom)
Return: ndarray  (subcarriers, N_rx)  complex64
"""
import struct, numpy as np

# ---------- Intel IWL5300 ----------------------------------------------------
INTEL_HDR = struct.Struct("<IIIIHHB")
INT16     = struct.Struct("<h")

def _parse_intel(buf: bytes):
    offs = INTEL_HDR.size + 2           # skip header + antenna info
    cmplx = []
    it = INT16.iter_unpack(buf[offs:])
    for re, im in zip(it, it):          # pair-wise
        cmplx.append(re[0] + 1j*im[0])
    nrx = 3
    nsc = len(cmplx) // nrx
    return np.array(cmplx, np.complex64).reshape(nsc, nrx)

# ---------- Nexmon -----------------------------------------------------------
def _parse_nexmon(buf: bytes):
    subc = int.from_bytes(buf[18:20], "little")
    data = np.frombuffer(buf, dtype="<f4", offset=20, count=subc*2)
    cmplx = data.view(np.complex64)
    return cmplx.reshape(subc, -1)

# ---------- ath9k (TL-WDR4300) ----------------------------------------------
def _parse_ath(buf: bytes):
    cmplx = np.frombuffer(buf, dtype="<i2").astype(np.float32).view(np.complex64)
    nrx   = 3 if len(cmplx) % 3 == 0 else 2
    nsc   = len(cmplx) // nrx
    return cmplx.reshape(nsc, nrx)

# ---------- Dispatcher -------------------------------------------------------
def parse_csi_radiotap(pkt) -> np.ndarray | None:
    if not pkt.haslayer("RadioTap") or not hasattr(pkt, "notdecoded"):
        return None
    raw = pkt.notdecoded
    if raw.startswith(b"\xa0\x00"):
        return _parse_intel(raw)
    if raw.startswith(b"\x4c\x08\x0b"):
        return _parse_nexmon(raw)
    if raw.startswith(b"\x00\x00\x20"):
        return _parse_ath(raw)
    return None
