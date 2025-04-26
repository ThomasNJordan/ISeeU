import numpy as np
from config import CHANNEL_BW, SPEED_OF_LIGHT

def cir_distance(csi_mat):
    """
    Coarse range from first path of channel impulse response.
    """
    if csi_mat is None:
        return None
    h = np.fft.ifft(csi_mat.mean(axis=1))
    idx = np.argmax(np.abs(h))
    delay = idx / CHANNEL_BW          # s
    return 0.5 * SPEED_OF_LIGHT * delay
