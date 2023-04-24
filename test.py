
import cv2
import numpy as np

# 1.获取相机内参数矩阵和畸变系数
K = np.array([[596.34925072, 0.0,         400.35710334],
              [0.0,        596.49697012, 300.47081541],
              [0.0,        0.0,         1.0]])
dist_coef = np.array([[9.86732100e-02, -4.94565440e-01,2.89052556e-04, 8.22459145e-01]])

object_points = np.array(
    [[-50, -50, 0], [-50, 50, 0], [50, -50, 0], [50, 50, 0]], dtype=np.float32)
image_points = np.array([[342.0, 423.0], [359.0, 447.25], [316.75, 439.25], [333.5, 464.0]], dtype=np.float32)


# 2.获取相机外参数
rvec, tvec = cv2.solvePnP(object_points, image_points, K, dist_coef)

# 3.将相机坐标转换为像素坐标
image_point, _ = cv2.projectPoints(object_points, rvec, tvec, K, dist_coef)

# 4.将像素坐标转换为归一化平面坐标
normalized_point = np.array(
    [image_point[0][0][0]/width, image_point[0][0][1]/height])

# 5.将归一化平面坐标转换为相机坐标
camera_point = np.dot(np.linalg.inv(
    K), np.concatenate((normalized_point, [1])))

# 6.将相机坐标转换为世界坐标
world_point = np.dot(np.linalg.inv(rvec), (camera_point - tvec))
