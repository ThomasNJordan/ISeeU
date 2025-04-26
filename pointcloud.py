import numpy as np

def polar_to_cartesian(r, theta_deg):
    theta = np.deg2rad(theta_deg)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = 0.0                    # 2-D slice; extend with elevation if you have it
    return np.array([x, y, z])

def build_pointcloud(distances, angles):
    pts = [polar_to_cartesian(d, a) for d, a in zip(distances, angles)]
    return np.vstack(pts)
