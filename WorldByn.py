"""
为了根据n幅图像(n > 4)和对应的四个点的三维世界坐标和二维像素坐标来求其他点的世界坐标,我们可以对之前的代码进行扩展。
首先,需要计算n个相机的姿态(旋转和平移矩阵),然后使用这些矩阵和相机内参矩阵进行三角测量,以计算其他点的三维世界坐标。
这里我们将使用两两图像组合进行三角测量,并对结果取平均值以获得更稳定的估计。
"""
import cv2
import numpy as np
import itertools

def estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs):
    _, rvec, tvec, _ = cv2.solvePnPRansac(world_coords, pixel_coords, camera_matrix, dist_coeffs)
    return rvec, tvec

def triangulate_points(pixel_coords1, pixel_coords2, camera_matrix, rvec1, tvec1, rvec2, tvec2):
    proj_matrix1 = np.dot(camera_matrix, np.hstack((cv2.Rodrigues(rvec1)[0], tvec1)))
    proj_matrix2 = np.dot(camera_matrix, np.hstack((cv2.Rodrigues(rvec2)[0], tvec2)))
    world_coords = cv2.triangulatePoints(proj_matrix1, proj_matrix2, pixel_coords1.T, pixel_coords2.T).T
    world_coords = (world_coords / world_coords[:, 3:])[:, :3]
    return world_coords

# n幅图像的世界坐标和像素坐标(需要根据实际情况进行替换)
world_coords_list = [
    # 请根据实际情况添加更多的世界坐标
]

pixel_coords_list = [
    # 请根据实际情况添加更多的像素坐标
]

# 相机内参矩阵和畸变系数(需要根据实际相机参数进行替换)
camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((4, 1), dtype=np.float32)

# 计算n幅图像的相机姿态
camera_poses = [estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs) for world_coords, pixel_coords in zip(world_coords_list, pixel_coords_list)]

# 示例：将图像1上的像素坐标 (100, 100) 转换为世界坐标
pixel_coord_example = (100, 100)
pixel_coords = np.array([pixel_coord_example], dtype=np.float32)

# 两两图像组合进行三角测量
triangulated_points = []
for (i, j) in itertools.combinations(range(len(camera_poses)), 2):
    rvec1, tvec1 = camera_poses[i]
    rvec2, tvec2 = camera_poses[j]
    world_coord = triangulate_points(pixel_coords, pixel_coords, camera_matrix, rvec1, tvec1, rvec2, tvec2)[0]
    triangulated_points.append(world_coord)

# 对结果取平均值
world_coord_example = np.mean(triangulated_points, axis=0)
print(f"Pixel coordinate {pixel_coord_example} in the n images corresponds to world coordinate {world_coord_example}")
