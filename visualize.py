import open3d as o3d, numpy as np

def show_pointcloud(pts: np.ndarray):
    if pts.size == 0:
        print("No points collected.")
        return
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(pts)
    o3d.visualization.draw_geometries([pc])
