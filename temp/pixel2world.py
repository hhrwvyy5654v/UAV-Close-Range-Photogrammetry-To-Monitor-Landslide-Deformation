import cv2
import numpy as np

# 世界坐标中的 3D 点
world_points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=np.float32)

# 图像坐标中的 2D 点
image_points = np.array([[10, 10], [20, 10], [10, 20], [10, 5]], dtype=np.float32)

# 相机矩阵
camera_matrix = np.array([[1000, 0, 320], [0, 1000, 240], [0, 0, 1]], dtype=np.float32)

# 失真系数
dist_coeffs = np.zeros((4,1))

# 解决 PnP 问题
success, rvec, tvec = cv2.solvePnP(world_points, image_points, camera_matrix, dist_coeffs)

# 将旋转矢量转换为旋转矩阵
R = cv2.Rodrigues(rvec)[0]

# 计算图像中心的世界坐标
image_center = np.array([320,240], dtype=np.float32)
world_center = -np.dot(np.linalg.inv(R), tvec)

# 计算图像角的世界坐标
image_corners = np.array([[0,0], [640,0], [640,480], [0,480]], dtype=np.float32)
world_corners = np.zeros((4,3), dtype=np.float32)
for i in range(4):
    ray = np.dot(np.linalg.inv(camera_matrix), np.array([image_corners[i][0], image_corners[i][1], 1]))
    ray /= np.linalg.norm(ray)
    world_corners[i] = -np.dot(np.linalg.inv(R), ray*tvec[2])

print("World center:", world_center)
print("World corners:", world_corners)