import cv2
import numpy as np

# 定义相机矩阵和畸变系数
mtx = np.array([[596.34925072, 0.0,         400.35710334],
        [0.0,        596.49697012, 300.47081541],
        [0.0,        0.0,         1.0]])
dist = np.array([[9.86732100e-02,-4.94565440e-01,-4.51708734e-04,2.89052556e-04,8.22459145e-01]])

# 定义像素坐标和相机矩阵
img_point = np.array([[342.0,423.0],[359.0,447.25],[316.75,439.25],[333.5,464.0]], dtype=np.float32)
camera_matrix = mtx

# 定义世界坐标系下的三维点
obj_point = np.array([[-50, -50, 0],[-50, 50, 0],[50, -50, 0],[50, 50, 0]], dtype=np.float32)

# 解算相机位姿
ret, rvec, tvec = cv2.solvePnP(obj_point, img_point, camera_matrix, dist)

# 将相机坐标转换为世界坐标
rot_mat, _ = cv2.Rodrigues(rvec)
world_point = -np.dot(rot_mat.T, tvec)

print(world_point)

