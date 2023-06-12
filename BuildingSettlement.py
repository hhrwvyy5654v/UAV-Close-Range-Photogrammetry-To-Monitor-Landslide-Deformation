'''
Description:  
FilePath: \BuildingSettlement.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-06-09 09:41:02
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-12 15:25:27
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import cv2
import numpy as np


def detect_aruco_markers(image_path, aruco_dict, marker_length, camera_matrix, dist_coeffs):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    aruco_params = cv2.aruco.DetectorParameters_create()
    corners, ids, _ = cv2.aruco.detectMarkers(
        gray, aruco_dict, parameters=aruco_params)

    if ids is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs)
        return corners, ids, rvecs, tvecs
    else:
        return None, None, None, None


def get_aruco_pose(corners, ids, rvecs, tvecs, target_id):
    index = np.where(ids == target_id)[0]
    if index.size > 0:
        rvec = rvecs[index][0]
        tvec = tvecs[index][0]
        return r, tvec
    else:
        return None, None


def main():
    # 预设参数
    marker_length = 0.1  # ArUco 标记的边长（单位：米）
    camera_matrix = np([[800, 0, 320], [0, 800, 240], [0, 0, 1]])  # 相机内参矩阵
    dist_coeffs = np.zeros((5, 1))  # 畸变系数

    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

    # 拍摄照片
    image_path = 'path/to/your/image.jpg'

    # 检测 ArUco 标记
    corners, ids, rvecs, tvecs = detect_aruco_markers(
        image_path, aruco_dict, marker_length, camera_matrix, dist_coeffs)

    if ids is not None:
        # 获取两个 ArUco 标记的位姿
        rvec1, tvec1 = get_aruco_pose(corners, ids, rvecs, tvecs, target_id=1)
        rvec2, tvec2 = get_aruco_pose(corners, ids, rvecs, tvecs, target_id=2)

        # 计算两个 ArUco 标记在相机坐标系下的三维坐标
        if rvec1 is not None and rvec2 is not:

            point1_cam = tvec1
            point2_cam = tvec2

            # 保存初始坐标
            initial_point1_cam = point1_cam.copy()
            initial_point2_cam = point2_cam.copy()

            # 建筑发生沉降后，重复上述操作
            # ...
            # final_point1_cam, final2_cam = ...

            # 计算两组标记点的 ArUco 码的世界坐标的差
            delta_point1 = final_point1_cam - initial_point1_cam
            delta_point2 = final_point2_cam - initial_point2_cam

            print(f'Delta Point 1: {delta_point1}')
            print(f'Delta Point 2: {delta_point2}')
        else:
            print('Target ArUco markers not found.')
    else:
        print('No ArUco markers found.')


if __name__ == '__main__':
    main()
