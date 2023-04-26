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


# 两幅图像的世界坐标和像素坐标
world_coords_list = [
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32),
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32)
]

pixel_coords_list = [
    np.array([[327.0, 462.75], [329.5, 431.0], [366.25, 463.0],
             [366.75, 432.0]], dtype=np.float32),
    np.array([[368.25, 481.0], [371.5, 447.25], [
             411.0, 484.0], [412.0, 450.0]], dtype=np.float32)
]

# 相机内参矩阵和畸变系数（需要根据实际相机参数进行替换）
camera_matrix = np.array([[596.34925072, 0, 400.35710334], [
                         0, 596.49697012, 300.47081541], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.array([9.86732100e-02, -4.94565440e-01, -4.51708736e-04,
                       2.89052555e-04, 8.22459145e-01], dtype=np.float32).reshape(5, 1)

# 计算两幅图像的相机姿态
camera_poses = [estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs)
                for world_coords, pixel_coords in zip(world_coords_list, pixel_coords_list)]


pixel_coord_example1 = (403.75, 433.0)
pixel_coord_example2 = (452.5, 452.5)

# pixel_coord_example1 = (405.25 , 463.75)
# pixel_coord_example2 = (454.0 , 486.5)
rvec1, tvec1 = camera_poses[0]
rvec2, tvec2 = camera_poses[1]
world_coord_example = triangulate_points(
    np.array([pixel_coord_example1], dtype=np.float32),
    np.array([pixel_coord_example2], dtype=np.float32),
    camera_matrix, rvec1, tvec1, rvec2, tvec2
)[0]

print(f"图像1的像素坐标{pixel_coord_example1}和图像2的像素坐标{pixel_coord_example2}所对应世界坐标:\n{world_coord_example}")
"""
根据两幅图像和图像上对应的四个点的世界坐标和像素坐标,求其它点的世界坐标。
"""
