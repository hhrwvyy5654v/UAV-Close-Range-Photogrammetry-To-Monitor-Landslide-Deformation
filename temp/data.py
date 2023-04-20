import cv2
import numpy as np
img1_path="./calibration_plate/original/IMG_1.jpg"

img=cv2.imread(img1_path)
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
w1,h1=(11,8)

cp_int = np.zeros((w1 * h1, 3), np.float32)
cp_int[:, :2] = np.mgrid[0:w1, 0:h1].T.reshape(-1, 2)
# cp_world:保存角点在世界空间的坐标。
cp_world = cp_int * 0.02

ret, cp_img = cv2.findChessboardCorners(gray_img, (w1,h1), None)
obj_points = []  # 世界空间中的点
img_points = []  # 图像空间中的点（与 obj_points 相关）
obj_points.append(cp_world)
img_points.append(cp_img)

# 查看角点
cv2.drawChessboardCorners(img, (w1,h1), cp_img, ret)
cv2.imwrite("test.jpg",img)

ret, mat_inter, coff_dis, v_rot, v_trans = cv2.calibrateCamera(obj_points, img_points, gray_img.shape[::-1], None, None)

print("内参=",mat_inter)
print("\n畸变系数=",coff_dis)
print("\n旋转向量=",v_rot)
print("\n平移向量=",v_trans)