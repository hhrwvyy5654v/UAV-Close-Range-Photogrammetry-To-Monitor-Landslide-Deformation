import os
import cv2
import numpy as np

# 定义棋盘格模板大小
pattern_size = (12, 9)

# 定义每个棋盘格的物理尺寸（单位：毫米）
square_size = 40.0

# 准备物体点坐标
object_points = []
for i in range(pattern_size[1]):
    for j in range(pattern_size[0]):
        object_points.append((j*square_size, i*square_size, 0))
object_points = np.array(object_points, dtype=np.float32)


# 找到棋盘格角点
image_points = []
cap = cv2.VideoCapture(0) # 打开摄像头
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, pattern_size)

    if ret:
        # 如果找到了棋盘格角点，则绘制并保存角点坐标
        cv2.drawChessboardCorners(frame, pattern_size, corners, ret)
        image_points.append(corners)
        
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 进行相机标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)

# 输出内参矩阵和畸变系数
print("内参矩阵：\n", mtx)
print("畸变系数：\n", dist)

# 输出每幅图像的旋转向量和平移向量
for i in range(len(rvecs)):
    print("第 %d 幅图像的旋转向量：" % (i+1), rvecs[i].ravel())
    print("第 %d 幅图像的平移向量：" % (i+1), tvecs[i].ravel())
