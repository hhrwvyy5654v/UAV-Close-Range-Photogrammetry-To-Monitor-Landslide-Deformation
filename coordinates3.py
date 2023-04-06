import cv2
import numpy as np

"""
其中,world_points是已知点的世界坐标,
image_points是已知点的图像坐标,
camera_matrix是相机内参矩阵,
rvec和tvec是相机外参矩阵
"""


# 已知点的世界坐标
world_points = np.array([
    [0, 0, 0], 
    [0, 200, 0], 
    [150, 0, 0], 
    [150, 200, 0]
], dtype=np.float32)

# 已知点的图像坐标
image_points = np.array([
    [100, 100],
    [200, 100],
    [200, 200],
    [100, 200]
], dtype=np.float32)

# 相机内参矩阵
camera_matrix = np.array([
    [755.39354935,0,504.39208928],
    [0,754.16550667,371.66825215],
    [0, 0, 1]
], dtype=np.float32)

# 相机外参矩阵
rvec = np.array([0, 0, 0], dtype=np.float32)
tvec = np.array([0, 0, -5], dtype=np.float32)

# 计算旋转矩阵
R = cv2.Rodrigues(rvec)[0]

# 计算投影矩阵
proj_matrix = np.hstack((R, tvec.reshape(3, -1)))
proj_matrix = np.dot(camera_matrix, proj_matrix)

# 计算其他点的世界坐标
other_points = cv2.triangulatePoints(
    proj_matrix[:, :3], proj_matrix[:, -1].reshape(3, -1),
    image_points.T.astype(np.float32), world_points.T.astype(np.float32)
).T

print(other_points)
