'''
Description: 
FilePath: \无人机建筑沉降监测\demo.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-06-06 11:44:10
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-06 14:16:08
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import cv2
import cv2.aruco as aruco
import numpy as np

# 加载npz文件读取相机的内参矩阵和畸变系数
data = np.load('./Parameter/豪威OV48B.npz') 

# 获取mtx和dist参数
camera_matrix = data['mtx']
dist_coeffs = data['dist']

# 已知的Aruco标记的世界坐标（请根据您的实际情况进行调整）
known_world_coords = {
    0: np.array([0, 0, 0]),
    1: np.array([1, 0, 0]),
    2: np.array([1, 1, 0]),
    3: np.array([0, 1, 0]),
}

def detect_aruco_markers(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    return corners, ids

def estimate_world_coordinates(corners, ids):
    world_coords = {}
    for i, corner in enumerate(corners):
        rvec, tvec, _ = cv2.solvePnP(
            np.float32([known_world_coords[ids[i][0]]]),
            np.float32(corner),
            camera_matrix,
            dist_coeffs,
        )
        world_coords[ids[i][0]] = tvec
    return world_coords

def main():
    # 读取两张图像
    image1 = cv2.imread("image1.jpg")
    image2 = cv2.imread("image2.jpg")

    # 检测Aruco标记
    corners1, ids1 = detect_aruco_markers(image1)
    corners2, ids2 = detect_aruco_markers(image2)

    # 估计世界坐标
    world_coords1 = estimate_world_coordinates(corners1, ids1)
    world_coords2 = estimate_world_coordinates(corners2, ids2)

    # 计算坐标变化
    for id in world_coords1:
        if id in world_coords2:
            delta = world_coords2[id] - world_coords1[id]
            print(f"Aruco marker {id} moved by {delta}")

if __name__ == "__main__":
    main()
