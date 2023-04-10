"""
1.通过相机拍摄到的图像,使用OpenCV中的aruco库检测和识别四个ArUco标记,并获取它们的像素坐标和ID。
2.根据相机内部参数和畸变参数,将像素坐标转换为相机坐标系下的坐标。
3.根据相机的外部参数(即相机的旋转矩阵和平移向量),将相机坐标系下的坐标转换为世界坐标系下的坐标。
4.利用四个ArUco标记的世界坐标,计算出第五个点的世界坐标。

具体方法可以是通过计算四个标记的中心点或者计算四个标记的交点来获取第五个点的世界坐标。

需要注意的是,计算世界坐标时需要使用相机的外部参数,因此您需要先进行相机标定,获取相机的内部参数和外部参数。
同时,识别ArUco标记时需要保证标记的大小、数量和布局是已知的,并且标记之间的距离和相机与标记的相对位置也是已知的。
"""
import cv2
import numpy as np
import cv2.aruco as aruco

# 相机内参数矩阵K和畸变参数dist
K = np.array([[755.39354935, 0, 504.39208928], [0, 754.16550667, 371.66825215], [0, 0, 1]])
dist = np.array([2.83890589e-01,-1.65886965e+00,4.88852246e-04,-4.33686303e-04,3.34750924e+00])

# aruco字典
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# aruco码尺寸
marker_size = 0.05  # 单位：米

# 第一幅图像和第二幅图像的文件名
img1_file = "./aruco_images/IMG_2575.jpg"
img2_file = "./aruco_images/IMG_2576.jpg"

# 读取第一幅图像和第二幅图像
img1 = cv2.imread(img1_file)
img2 = cv2.imread(img2_file)

# 使用aruco库检测第一幅图像和第二幅图像中的aruco码,并获取四个点的图像坐标和世界坐标系中的坐标
corners1, ids1, _ = aruco.detectMarkers(image=img1, dictionary=aruco_dict)
corners2, ids2, _ = aruco.detectMarkers(image=img2, dictionary=aruco_dict)

retval1, rvec1, tvec1 = aruco.estimatePoseSingleMarkers(
    corners1, marker_size, K, dist)

retval2, rvec2, tvec2 = aruco.estimatePoseSingleMarkers(
    corners2, marker_size, K, dist)

P1, P2, P3, P4 = np.array(
    [[-5, -5, 0], [-5, 5, 0], [5, 5, 0], [5, 5, 0]]) * marker_size
world_corners1 = np.array([P1, P2, P3, P4])
world_corners2 = np.array([np.squeeze(cv2.projectPoints(np.array([[[0, 0, 0]]]), rvec1, tvec1, K, dist)[0]),
                           np.squeeze(cv2.projectPoints(np.array([[[marker_size, 0, 0]]]), rvec1, tvec1, K, dist)[0]),
                           np.squeeze(cv2.projectPoints(np.array([[[marker_size, marker_size, 0]]]), rvec1, tvec1, K, dist)[0]),
                           np.squeeze(cv2.projectPoints(np.array([[[0, marker_size, 0]]]), rvec1, tvec1, K, dist)[0])])

# 使用PnP算法和三角测量方法计算其它点的世界坐标
# 首先,将四个点的图像坐标和世界坐标系中的坐标转换为numpy数组
image_points = np.array([corners1[0][0], corners1[0][1],
                        corners1[0][2], corners1[0][3]], dtype="float")
world_points = np.array([world_corners1[0], world_corners1[1],
                        world_corners1[2], world_corners1[3]], dtype="float")

# 使用solvePnP函数计算第一幅图像的相机位姿
retval, rvec, tvec = cv2.solvePnP(world_points, image_points, K, dist)

# 将其它点的图像坐标转换为numpy数组
other_points_image = np.array(
    [[5, 10], [-5, 10]], dtype="float")

# 使用projectPoints函数将其它点的图像坐标转换为世界坐标系中的坐标
other_points_world = cv2.projectPoints(
    other_points_image, rvec, tvec, K, dist)[0]

# 输出其它点的世界坐标
print("其它点的世界坐标:")
for i, point in enumerate(other_points_world):
    print("Point {}: ({}, {}, {})".format(
        i+1, point[0][0], point[0][1], point[0][2]))
