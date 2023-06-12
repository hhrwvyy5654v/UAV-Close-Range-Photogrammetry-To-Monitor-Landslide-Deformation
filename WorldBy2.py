'''
Description: 根据两幅图像上对应的四个点的世界坐标系下的点坐标和相机坐标系下的像素坐标来求其他点的世界坐标
FilePath: \WorldBy2.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-05-03 18:37:15
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-12 14:41:26
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
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
    np.array([[-37.33, -37.33, 0], [-37.33, 37.33, 0], [37.33, -37.33, 0],
             [37.33, 37.33, 0]], dtype=np.float32),
    np.array([[-37.33, -37.33, 0], [-37.33, 37.33, 0], [37.33, -37.33, 0],
             [37.33, 37.33, 0]], dtype=np.float32)
]

pixel_coords_list = [
    # DSC00108.JPG
    np.array([[4867.5, 2703.5], [4572.75, 2703.75], [4865.25, 2389.5],
             [4572.0, 2388.25]], dtype=np.float32),
    # DSC00109.JPG
    np.array([[4833.5, 2727.0], [4534.0, 2723.5],
              [4837.25, 2414.0], [4537.0, 2412.75]], dtype=np.float32)
]

# 加载npz文件读取相机的内参矩阵和畸变系数
data = np.load('./Parameter/豪威OV48B_8000x6000.npz')

# 获取mtx和dist参数
camera_matrix = data['mtx']
dist_coeffs = data['dist']

# 计算两幅图像的相机姿态
camera_poses = [estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs)
                for world_coords, pixel_coords in zip(world_coords_list, pixel_coords_list)]

# 获取每幅图像的旋转向量rvec和平移向量tvec
rvec1, tvec1 = camera_poses[0]
rvec2, tvec2 = camera_poses[1]


# id[4]
pixel_coord_example1 = (4862.75, 2076.0)
pixel_coord_example2 = (4841.5, 2100.75)

# id[5]
# pixel_coord_example1 = (4569.75,2072.0)
# pixel_coord_example2 = (4541.25,2100.75)

world_coord_example = triangulate_points(
    np.array([pixel_coord_example1], dtype=np.float32),
    np.array([pixel_coord_example2], dtype=np.float32),
    camera_matrix, rvec1, tvec1, rvec2, tvec2
)[0]

print(f"图像1的像素坐标{pixel_coord_example1}和图像2的像素坐标{pixel_coord_example2}所对应世界坐标:\n{world_coord_example}")
