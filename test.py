import cv2
import numpy as np

# 检测Aruco码并估计相机姿态


def detect_aruco_markers(image, aruco_dict, camera_matrix, dist_coeffs):
    aruco_params = cv2.aruco.DetectorParameters_create()
    corners, ids, _ = cv2.aruco.detectMarkers(
        image, aruco_dict, parameters=aruco_params)
    if ids is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs)
        return corners, ids, rvecs, tvecs
    else:
        return None, None, None, None


# 读取图像
image1 = cv2.imread('./Aruco/IMG_20230425_171500.jpg')
image2 = cv2.imread('./Aruco/IMG_20230426_110858.jpg')

# Aruco字典
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# 加载npz文件读取相机的内参矩阵和畸变系数
data = np.load('./Parameter/豪威OV48B.npz')

# 获取mtx和dist参数
camera_matrix = data['mtx']
dist_coeffs = data['dist']


marker_length = 0.04  # Aruco码的实际尺寸（单位：米）

# 检测Aruco码并估计相机姿态
corners1, ids1, rvecs1, tvecs1 = detect_aruco_markers(
    image1, aruco_dict, camera_matrix, dist_coeffs)
corners2, ids2, rvecs2, tvecs2 = detect_aruco_markers(
    image2, aruco_dict, camera_matrix, dist_coeffs)

# 计算滑坡区域的位移（需要根据实际情况进行调整）
if ids1 is not None and ids2 is not None:
    for i, id1 in enumerate(ids1):
        for j, id2 in enumerate(ids2):
            if id1 == id2:
                displacement = np.linalg.norm(tvecs1[i] - tvecs2[j])
                print(
                    f'Marker {id1}: Displacement = {displacement:.2f} meters')
