'''
Description: 识别Aruco码的像素坐标,结合预设置的世界坐标,计算相机的旋转向量R和平移向量T
FilePath: \GetR&T.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-06-12 14:44:18
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-14 15:23:52
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import cv2
import numpy as np

# 读取包含两个aruco码的照片
image = cv2.imread('ArucoShot\800x600\IMG_20230614_145326.jpg')

# 定义aruco字典和参数
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

# 检测aruco码
corners, ids, _ = cv2.aruco.detectMarkers(
    image, aruco_dict, parameters=parameters)

# 预设的世界坐标(Aruco码中心点的世界坐标)
world_coordinates = np.array([
    [0, 0, 0],
    [0, 0, 0],
], dtype=np.float32)

# 加载npz文件读取相机的内参矩阵和畸变系数
data = np.load('./Parameter/豪威OV48B_800x600.npz')

# 获取mtx和dist参数
camera_matrix = data['mtx']
dist_coeffs = data['dist']


# aruco码的实际尺寸（单位：米）
marker_length = 0.05

# 计算相机的旋转参数R和平移参数T
retval, rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(
    corners, marker_length, camera_matrix, dist_coeffs)

# 输出结果
for i, (rvec, tvec) in enumerate(zip(rvecs, tvecs)):
    print(f"Aruco码 {ids[i]} 的旋转向量：\n{rvec}\n平移向量:\n{tvec}\n")
