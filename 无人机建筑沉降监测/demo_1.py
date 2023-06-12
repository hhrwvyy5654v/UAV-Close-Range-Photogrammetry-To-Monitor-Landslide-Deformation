'''
Description: 
FilePath: \无人机建筑沉降监测\demo_1.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-06-09 09:32:16
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-09 09:34:15
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import cv2
import numpy as np
from cv2 import aruco

# 读取照片
image = cv2.imread("path/to/your/image.jpg")

# 设置aruco字典和参数
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

# 检测aruco码
corners, ids, _ = aruco.detectMarkers(image, aruco_dict, parameters=parameters)

# 预设的世界坐标
world_coordinates = np.array([
    [0, 0, 0],
    [1, 0, 0]
], dtype=np.float32)

# 加载npz文件读取相机的内参矩阵和畸变系数
data = np.load('./Parameter/豪威OV48B.npz')

# 获取mtx和dist参数
camera_matrix = data['mtx']
dist_coeffs = data['dist']

# 计算外参信息
rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
    corners, 1, camera_matrix, dist_coeffs)

# 计算两个aruco码在相机坐标系下的三维坐标
aruco_3d_coordinates = []
for rvec, tvec in zip(rvecs, tvecs):
    R, _ = cv2.Rodrigues(rvec)
    aruco_3d_coordinate = np.matmul(R, world_coordinates.T) + tvec
    aruco_3d_coordinates.append(aruco_3d_coordinate.T)

aruco_3d_coordinates = np.array(aruco_3d_coordinates)

print("Aruco 1 3D coordinate:", aruco_3d_coordinates[0])
print("Aruco 2 3D coordinate:", aruco_3d_coordinates[1])
