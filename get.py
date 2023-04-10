import cv2
import cv2.aruco as aruco

# 加载图像
image = cv2.imread("./aruco_images/微信图片_20230410165039.jpg")

# 定义字典和参数
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

# 检测图像中的标记
corners, ids, rejectedImgPoints = aruco.detectMarkers(image, aruco_dict, parameters=parameters)

# 打印检测到的标记的角和 ID
if len(corners) > 0:
    print("检测到的标记:")
    for i in range(len(corners)):
        print(f"标记{ids[i]}的角点为:\n {corners[i]}")
else:
    print("未检测到标记物")