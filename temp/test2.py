import cv2
import numpy as np


def calculate_world_coordinates(image_points1, image_points2, world_points, target_image_points1, target_image_points2):
    # 将输入转换为numpy数组
    image_points1 = np.array(image_points1, dtype=np.float32)
    image_points2 = np.array(image_points2, dtype=np.float32)
    world_points = np.array(world_points, dtype=np.float32)
    target_image_points1 = np.array(target_image_points1, dtype=np.float32)
    target_image_points2 = np.array(target_image_points2, dtype=np.float32)

    # 使用已知的四个点计算单应性矩阵
    H1, _ = cv2.findHomography(image_points1, world_points)
    H2, _ = cv2.findHomography(image_points2, world_points)

    # 使用单应性矩阵计算目标点的世界坐标
    target_world_points1 = cv2.perspectiveTransform(
        target_image_points1.reshape(-1, 1, 2), H1)
    target_world_points2 = cv2.perspectiveTransform(
        target_image_points2.reshape(-1, 1, 2), H2)

    # 将结果转换为原始形状
    target_world_points1 = target_world_points1.reshape(-1, 2)
    target_world_points2 = target_world_points2.reshape(-1, 2)

    return target_world_points1, target_world_points2


# 已知的四个点的像素坐标和世界坐标
image_points1 = [(342.0, 423.0), (359.0, 447.25),
                 (316.75, 439.25), (333.5, 464.0)]
image_points2 = [(415.0, 417.0), (436.0, 437.5),
                 (394.0, 436.5), (415.0, 457.0)]
world_points = [(-50, -50, 0), (-50, 50, 0), (50, -50, 0), (50, 50, 0)]

# 要计算世界坐标的目标点的像素坐标
target_image_points1 = [(290.0, 456.0), (306.5, 481.75)]
target_image_points2 = [(371.75, 456.0), (393.0, 478.0)]

# 计算目标点的世界坐标
target_world_points1, target_world_points2 = calculate_world_coordinates(
    image_points1, image_points2, world_points, target_image_points1, target_image_points2)

print("id[4]和id[5]在image 1的世界坐标的(x,y):\n", target_world_points1)
print("id[4]和id[5]在image 2的世界坐标的(x,y):\n", target_world_points2)
