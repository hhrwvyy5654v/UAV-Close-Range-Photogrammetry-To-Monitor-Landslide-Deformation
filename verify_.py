import cv2
import numpy as np

# 读取相机参数
camera_matrix = np.array([[755.39354935, 0, 504.39208928], [
                         0, 754.16550667, 371.66825215], [0, 0, 1]])
dist_coeffs = np.array([2.83890589e-01, -1.65886965e+00,
                       4.88852246e-04, -4.33686303e-04, 3.34750924e+00])
# 读取图像
img1 = cv2.imread("./aruco_images/IMG_2575.jpg")
img2 = cv2.imread("./aruco_images/IMG_2576.jpg")

# 定义ArUco字典
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# 创建ArUco检测器
aruco_params = cv2.aruco.DetectorParameters_create()

# 检测ArUco标记
corners1, ids1, _ = cv2.aruco.detectMarkers(
    img1, aruco_dict, parameters=aruco_params)
corners2, ids2, _ = cv2.aruco.detectMarkers(
    img2, aruco_dict, parameters=aruco_params)

# 计算旋转矩阵和平移向量
rvecs1, tvecs1, _ = cv2.aruco.estimatePoseSingleMarkers(
    corners1, 0.05, camera_matrix, dist_coeffs)
rvecs2, tvecs2, _ = cv2.aruco.estimatePoseSingleMarkers(
    corners2, 0.05, camera_matrix, dist_coeffs)

# 将像素坐标转换为相机坐标系下的坐标
object_points = np.array([[0, 0, 0], [0.05, 0, 0], [0.05, 0.05, 0], [
                         0, 0.05, 0]], dtype=np.float32)
image_points1 = np.squeeze(corners1)
image_points2 = np.squeeze(corners2)

# imagePoints, jacobian = cv.projectPoints(np.array(obj_points),np.float32(rvec), np.float32(tvec),camera_matrix1, None)
camera_points1, _ = cv2.projectPoints(
    object_points, rvecs1, tvecs1, camera_matrix, dist_coeffs)
camera_points2, _ = cv2.projectPoints(
    object_points, rvecs2, tvecs2, camera_matrix, dist_coeffs)

# 将相机坐标系下的点转换为世界坐标系下的点
R1, _ = cv2.Rodrigues(rvecs1)
R2, _ = cv2.Rodrigues(rvecs2)
t1 = tvecs1.reshape(-1)
t2 = tvecs2.reshape(-1)
world_point1 = np.dot(R1.T, camera_points1[0].reshape(-1) - t1)
world_point2 = np.dot(R2.T, camera_points2[0].reshape(-1) - t2)
world_point5 = np.dot(R2.T, camera_points2[3].reshape(-1) - t2)

# 打印第五个点的世界坐标
print("第五个点的世界坐标：", world_point5.reshape(-1))
