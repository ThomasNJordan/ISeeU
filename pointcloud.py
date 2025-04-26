import numpy as np

def pol_to_cart(r, theta_deg):
    th = np.deg2rad(theta_deg)
    return np.array([r*np.cos(th), r*np.sin(th), 0.0])

def build_cloud(rs, thetas):
    pts = [pol_to_cart(r, t) for r, t in zip(rs, thetas)]
    return np.vstack(pts) if pts else np.empty((0,3))
