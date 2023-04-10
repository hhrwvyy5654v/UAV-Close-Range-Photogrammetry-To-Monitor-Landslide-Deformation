import cv2
import numpy as np

# 加载用于生成标记的字典
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# 使用默认值初始化检测器参数
parameters = cv2.aruco.DetectorParameters_create()

# 加载包含 ArUco 标记的图像
image = cv2.imread('./aruco_images/IMG_2575.jpg')

# 检测图像中的标记
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image, dictionary, parameters=parameters)

# 在图像上绘制检测到的标记
image = cv2.aruco.drawDetectedMarkers(image, corners)




# 计算每个标记的中心点
for i in range(len(corners)):
    # 获取当前标记的角
    markerCorners = corners[i][0]

    # 计算当前标记的中心点
    center = np.mean(markerCorners, axis=0)

    # 打印当前标记的中心点
    print("Marker", ids[i], "center:", center)
    print(center[0],center[1])
    
