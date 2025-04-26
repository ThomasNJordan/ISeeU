import open3d as o3d
import numpy as np

def show_pointcloud(pts: np.ndarray):
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(pts)
    o3d.visualization.draw_geometries([pc])
