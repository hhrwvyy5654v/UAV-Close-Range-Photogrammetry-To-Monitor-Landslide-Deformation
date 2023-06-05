'''
Description: 
FilePath: \Verify\WorldBy2_plus.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-05-31 15:16:13
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-05-31 15:57:04
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import numpy as np
import cv2

# 相机内参矩阵和畸变系数
camera_matrix = np.array([[5.93153721e+03, 0, 3.98548663e+03], [0, 5.93372510e+03, 3.01964347e+03], [0, 0, 1]])
dist_coeffs = np.array([1.10554877e-01, -5.50039001e-01, -
                       6.17096842e-04, -3.07625014e-05, 8.96475008e-01])

# 图像尺寸
image_size = (8000, 6000)

# 世界坐标系下的四组对应点
world_pts = np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0], [50, 50, 0]])
pixel_pts1 = np.array([[3708.25, 2139.75], [3698.0, 1798.0], 
                       [4044.75, 2133.75],[4036.25, 1792.0]])
pixel_pts2 = np.array([[3938.75, 1794.25], [3941.0, 1479.5],
                       [4243.25, 1793.25], [4247.0, 1479.25]])

# 计算基础矩阵和本质矩阵
F, _ = cv2.findFundamentalMat(pixel_pts1, pixel_pts2)
E = np.dot(np.dot(camera_matrix.T, F), camera_matrix)

# 三角测量
_, R, T, _ = cv2.recoverPose(E, pixel_pts1, pixel_pts2, camera_matrix)
proj_mat1 = np.dot(camera_matrix, np.hstack([np.eye(3), np.zeros((3, 1))]))
proj_mat2 = np.dot(camera_matrix, np.hstack([R, T]))
homogeneous_pts1 = cv2.convertPointsToHomogeneous(pixel_pts1)
homogeneous_pts2 = cv2.convertPointsToHomogeneous(pixel_pts2)
pts3d_homogeneous = cv2.triangulatePoints(
    proj_mat1, proj_mat2, homogeneous_pts1.transpose(), homogeneous_pts2.transpose())
pts3d = cv2.convertPointsFromHomogeneous(pts3d_homogeneous.transpose())

# 获取其它点的世界坐标
x, y = 4379.25, 2125.75  # 需要获取世界坐标的像素点坐标
px = np.array([[x], [y], [1]])  # 归一化坐标系下的坐标
px_homogeneous = np.dot(np.linalg.inv(F), px)
px_homogeneous = np.append(px_homogeneous, 1)
px_homogeneous = px_homogeneous[:, np.newaxis]
px_homogeneous = np.dot(np.linalg.inv(camera_matrix), px_homogeneous)
px_homogeneous = np.append(px_homogeneous, 1)
px_homogeneous = px_homogeneous[:, np.newaxis]
px_homogeneous = np.dot(np.linalg.inv(proj_mat1), px_homogeneous)
px_homogeneous = np.append(px_homogeneous, 1)
px_homogeneous = px_homogeneous[:, np.newaxis]
px_homogeneous = np.dot(proj_mat2, px_homogeneous)
px_3d = px_homogeneous[0:3]/px_homogeneous[3]
print("World coordinates of pixel ({}, {}): {}".format(x, y, px_3d))
