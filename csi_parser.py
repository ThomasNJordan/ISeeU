import numpy as np
from CSIKit import read_pcap

def aoa_from_csi(csi_mat, d=0.03, f=5.18e9):
    """
    Simple Bartlett beamformer on a 2-antenna array → AoA estimate.
    csi_mat shape: (subcarriers, rx_antennas)
    """
    wavelength = 3e8 / f
    steering_angles = np.linspace(-90, 90, 181)
    responses = []
    for theta in steering_angles:
        a = np.exp(-1j*2*np.pi*d*np.sin(np.deg2rad(theta))/wavelength*np.arange(csi_mat.shape[1]))
        power = np.abs((csi_mat @ a.conj().T)**2).sum()
        responses.append(power)
    return steering_angles[int(np.argmax(responses))]
