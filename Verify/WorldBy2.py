import cv2
import numpy as np


def estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs):
    # 使用PnP算法估计相机姿态
    _, rvec, tvec, _ = cv2.solvePnPRansac(
        world_coords, pixel_coords, camera_matrix, dist_coeffs)
    return rvec, tvec


def triangulate_points(pixel_coords1, pixel_coords2, camera_matrix, rvec1, tvec1, rvec2, tvec2):
    # 三角测量计算世界坐标
    proj_matrix1 = np.dot(camera_matrix, np.hstack(
        (cv2.Rodrigues(rvec1)[0], tvec1)))
    proj_matrix2 = np.dot(camera_matrix, np.hstack(
        (cv2.Rodrigues(rvec2)[0], tvec2)))
    world_coords = cv2.triangulatePoints(
        proj_matrix1, proj_matrix2, pixel_coords1.T, pixel_coords2.T).T
    world_coords = (world_coords / world_coords[:, 3:])[:, :3]
    return world_coords


# 两幅图像中对应的世界坐标和像素坐标
world_coords_list = [
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32),
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32)
]

pixel_coords_list = [
    np.array([[3708.25,2139.75], [3698.0,1798.0], [4044.75,2133.75],
             [4036.25,1792.0]], dtype=np.float32),
    np.array([[3938.75,1794.25], [3941.0,1479.5], 
              [4243.25,1793.25], [4247.0,1479.25 ]], dtype=np.float32)
]

# 相机内参矩阵和畸变系数（需要根据实际相机参数进行替换）
camera_matrix = np.array([[5.93153721e+03,0,3.98548663e+03], 
                          [0,5.93372510e+03,3.01964347e+03], 
                          [0,0,1]], dtype=np.float32)
dist_coeffs = np.array([1.10554877e-01,-5.50039001e-01,-6.17096842e-04,-3.07625014e-05,8.96475008e-01], dtype=np.float32).reshape(5, 1)

# 计算两幅图像的相机姿态
camera_poses = [estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs)
                for world_coords, pixel_coords in zip(world_coords_list, pixel_coords_list)]
# 获取每幅图像的旋转向量rvec和平移向量tvec
rvec1, tvec1 = camera_poses[0]
rvec2, tvec2 = camera_poses[1]


pixel_coord_example1 = (4371.5,1786.25)
pixel_coord_example2 = (4551.75,1476.5)

# pixel_coord_example1 = (4379.25,2125.75)
# pixel_coord_example2 = (4547.25,1791.0)

world_coord_example = triangulate_points(
    np.array([pixel_coord_example1], dtype=np.float32),
    np.array([pixel_coord_example2], dtype=np.float32),
    camera_matrix, rvec1, tvec1, rvec2, tvec2
)[0]

print(f"图像1的像素坐标{pixel_coord_example1}和图像2的像素坐标{pixel_coord_example2}所对应世界坐标:\n{world_coord_example}")

