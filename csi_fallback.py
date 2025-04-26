"""
Tiny, stand-alone CSI decoder.

Many CSI libraries (e.g. CSIKit) are feature-rich but heavy.  Here we only
need *phase* across receive chains, so we parse the three most common
vendor Radiotap TLVs directly:

╭────────────┬─────────────────────────────┬──────────────────╮
│   Vendor   │  Chipsets                   │  Magic bytes     │
├────────────┼─────────────────────────────┼──────────────────┤
│ Intel 5300 │ 5300/6300 mini-PCIe         │ a0 00 …          │
│ Broadcom   │ Nexmon patch (e.g. BCM4358) │ 4c 08 0b …       │
│ Atheros    │ ath9k CSI Tool patch        │ 00 00 20 …       │
╰────────────┴─────────────────────────────┴──────────────────╯

`parse_csi(pkt) → ndarray` where shape = (subcarriers, N_rx)
"""
import numpy as np, struct

# ------------------------------------------------------------------ Intel 5300
IWL_HDR = struct.Struct("<IIIIHHB")    # fixed part of iwl_internal_csi_hdr
def _intel(buf: bytes):
    """
    Intel format = header (28 B) + antenna flags (2 B) + 30×3 complex int16
    We ignore the metadata—just unpack the IQ pairs.
    """
    off = IWL_HDR.size + 2
    it  = struct.iter_unpack("<h", buf[off:])     # little-endian int16 stream
    # Pair consecutive (real, imag) → complex
    vals = [re[0] + 1j * next(it)[0] for re in it]
    return np.array(vals, np.complex64).reshape(-1, 3)   # 30 SC × 3 RX

# ------------------------------------------------------------------ Nexmon CSI
def _nexmon(buf: bytes):
    """
    Nexmon embeds floats:   header(20 B) then subcarriers × (real, imag) float32.
    """
    n_sc = int.from_bytes(buf[18:20], "little")
    data = np.frombuffer(buf, "<f4", offset=20, count=n_sc * 2)
    return data.view(np.complex64).reshape(n_sc, -1)

# ------------------------------------------------------------------ ath9k CSI
def _ath(buf: bytes):
    """
    Atheros CSI Tool: raw int16 (real, imag) for each RX chain.  Packet size
    determines if it's 2 or 3 spatial streams.
    """
    vals = np.frombuffer(buf, "<i2").astype(np.float32).view(np.complex64)
    n_rx = 3 if len(vals) % 3 == 0 else 2
    return vals.reshape(-1, n_rx)

# ---------------------------------------------------------------- dispatcher
def parse_csi(pkt):
    """
    Return CSI ndarray if packet carries a supported vendor TLV.
    Otherwise return None so callers can skip it gracefully.
    """
    if not hasattr(pkt, "notdecoded"):   # scapy puts vendor data here
        return None
    raw = pkt.notdecoded
    if raw.startswith(b"\xa0\x00"):
        return _intel(raw)
    if raw.startswith(b"\x4c\x08\x0b"):
        return _nexmon(raw)
    if raw.startswith(b"\x00\x00\x20"):
        return _ath(raw)
    return None
