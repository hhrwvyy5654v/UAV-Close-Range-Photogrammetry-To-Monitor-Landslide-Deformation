import cv2
import numpy as np

def calculate_world_coordinates(image_points1, image_points2, image_points3, image_points4, world_points, target_image_points1, target_image_points2, target_image_points3, target_image_points4):
    # 将输入转换为numpy数组
    image_points1 = np.array(image_points1, dtype=np.float32)
    image_points2 = np.array(image_points2, dtype=np.float32)
    image_points3 = np.array(image_points3, dtype=np.float32)
    image_points4 = np.array(image_points4, dtype=np.float32)
    world_points = np.array(world_points, dtype=np.float32)
    target_image_points1 = np.array(target_image_points1, dtype=np.float32)
    target_image_points2 = np.array(target_image_points2, dtype=np.float32)
    target_image_points3 = np.array(target_image_points3, dtype=np.float32)
    target_image_points4 = np.array(target_image_points4, dtype=np.float32)

    # 使用已知的四个点计算单应性矩阵
    H1, _ = cv2.findHomography(image_points1, world_points)
    H2, _ = cv2.findHomography(image_points2, world_points)
    H3, _ = cv2.findHomography(image_points3, world_points)
    H4, _ = cv2.findHomography(image_points4, world_points)

    # 使用单应性矩阵计算目标点的归一化坐标
    target_normalized_points1 = cv2.perspectiveTransform(target_image_points1.reshape(-1, 1, 2), H1)
    target_normalized_points2 = cv2.perspectiveTransform(target_image_points2.reshape(-1, 1, 2), H2)
    target_normalized_points3 = cv2.perspectiveTransform(target_image_points3.reshape(-1, 1, 2), H3)
    target_normalized_points4 = cv2.perspectiveTransform(target_image_points4.reshape(-1, 1, 2), H4)

    # 将归一化坐标转换为齐次坐标
    target_homogeneous_points1 = np.hstack((target_normalized_points1, np.ones((target_normalized_points1.shape[0], 1))))
    target_homogeneous_points2 = np.hstack((target_normalized_points2, np.ones((target_normalized_points2.shape[0], 1))))
    target_homogeneous_points3 = np.hstack((target_normalized_points3, np.ones((target_normalized_points3.shape[0], 1))))
    target_homogeneous_points4 = np.hstack((target_normalized_points4, np.ones((target_normalized_points4.shape[0], 1))))

    # 使用四幅图像的投影矩阵计算目标点的三维坐标
    P1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=np.float32)
    P2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=np.float32)
    P3 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=np.float32)
    P4 = cv2.triangulatePoints(P1, P2, target_homogeneous_points1.T, target_homogeneous_points2.T)
    P4 = cv2.triangulatePoints(P4, P3, target_homogeneous_points3.T, target_homogeneous_points4.T)

    # 将结果转换为原始形状
    target_world_points = cv2.convertPointsFromHomogeneous(P4.T.reshape(-1, 4))

    return target_world_points.squeeze()

# 已知的四个点的像素坐标和世界坐标
image_points1 = [(100, 100), (200, 100), (100, 200), (200, 200)]
image_points2 = [(150, 150), (250, 150), (150, 250), (250, 250)]
image_points3 = [(200, 200), (300, 200), (200, 300), (300, 300)]
image_points4 = [(250, 250), (350, 250), (250, 350), (350, 350)]
world_points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]

# 要计算世界坐标的目标点的像素坐标
target_image_points1 = [(120, 120), (180, 120)]
target_image_points2 = [(170, 170), (230, 170)]
target_image_points3 = [(220, 220), (280, 220)]
target_image_points4 = [(270, 270), (330, 270)]

# 计算目标点的世界坐标
target_world_points = calculate_world_coordinates(image_points1, image_points2, image_points3, image_points4, world_points, target_image_points1, target_image_points2, target_image_points3, target_image_points4)

print("Target world points:", target_world_points)
