import numpy as np
from csi_fallback import parse_csi_radiotap
from config import ANTENNA_SPACING, CENTER_FREQUENCY

def aoa_from_pkt(pkt) -> float | None:
    """
    Bartlett beam-form on CSI ⇒ azimuth θ (deg).  Needs ≥2 RX chains.
    """
    csi = parse_csi_radiotap(pkt)
    if csi is None or csi.shape[1] < 2:
        return None

    lamb  = 3e8 / CENTER_FREQUENCY
    theta = np.linspace(-90, 90, 181)
    pwr   = []
    for ang in theta:
        a = np.exp(-1j*2*np.pi*ANTENNA_SPACING*np.sin(np.deg2rad(ang))/lamb
                   * np.arange(csi.shape[1]))
        pwr.append(np.abs((csi @ a.conj().T)**2).sum())
    return float(theta[int(np.argmax(pwr))]), csi   # return csi for CIR
