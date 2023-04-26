"""
通过已知的内参矩阵和畸变参数，
求得从世界坐标系变化到相机坐标系的旋转、平移向量,
进而得到相对位姿
"""

# 加载相机标定的内参数、畸变参数
from math import degrees as dg
import numpy as np
import cv2


with np.load('./Parameter/豪威OV48B.npz') as X:
    mtx, dist, rvecs, tvecs = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
print('已知内容：')
print('内参', mtx)
print('畸变参数', dist)

# 棋盘格模板规格,只算内角点个数,不算最外面的一圈点
width = 11
height = 8

# 世界坐标系下的物体位置矩阵（Z=0）
world_points = np.zeros((width * height, 3), dtype=np.float32)
world_points[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)


# 读取图片
test_img = cv2.imread('./CalibrationPlate/resize/IMG_20230420_153254.jpg')
gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)


# 找到图像平面点角点坐标
ret, image_points = cv2.findChessboardCorners(gray, (height, width), None)
if ret:
    retval, rvec, tvec = cv2.solvePnP(world_points, image_points, mtx, dist)
    print("retavl:", retval)
    print("旋转向量:", rvec)
    print("平移向量", tvec)

sita_x = dg(rvec[0][0])
sita_y = dg(rvec[1][0])
sita_z = dg(rvec[2][0])
print("sita_x is  ", sita_x)
print("sita_y is  ", sita_y)
print("sita_z is  ", sita_z)
