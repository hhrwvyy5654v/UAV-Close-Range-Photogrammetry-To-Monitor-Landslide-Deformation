"""
为了实现前后两个时间点的三维形变分析,
你需要首先确定两个时间点的图像上相应的点。
这可以通过特征匹配或光流等方法实现。
然后,使用已知的三维世界坐标和二维像素坐标计算其他点的世界坐标。
最后,比较两个时间点的世界坐标来分析形变。

这个示例代码首先在两个时间点的图像上找到相应的点。
然后使用已知的三维世界坐标和二维像素坐标计算其他点的世界坐标。
最后,比较两个时间点的世界坐标来分析形变。
请注意,这个示例代码假设你已经有了相机矩阵(内参)。
实际应用中,你可能需要根据你的相机参数进行调整。
此外,这个示例代码使用SIFT特征和FLANN匹配器来找到相应的点,
你可以根据需要使用其他特征检测和匹配方法。
"""


import cv2
import numpy as np


def find_corresponding_points(img1, img2):
    # 从两张图片中检测并提取特征
    detector = cv2.SIFT_create()
    keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(img2, None)

    # 使用基于 FLANN 的匹配器匹配特征
    matcher = cv2.FlannBasedMatcher(
        dict(algorithm=1, trees=5), dict(checks=50))
    matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

    # 应用比率测试来过滤良好的匹配
    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]
    points1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches])
    points2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches])

    return points1, points2


def compute_3d_coordinates(points, known_3d_coords, known_2d_coords, camera_matrix):
    # 查找已知二维坐标和检测到的二维点之间的单应性
    _, homography = cv2.findHomography(known_2d_coords, points)

    # 计算检测点的 3D 坐标
    points_3d = []
    for pt in points:
        pt_homogeneous = np.append(pt, 1)
        world_coord = np.dot(np.linalg.inv(homography), pt_homogeneous)
        world_coord /= world_coord[-1]
        points_3d.append(world_coord[:3])

    return np.array(points_3d)


def compute_3d_coordinates(points, known_3d_coords, known_2d_coords, camera_matrix):
    # Find homography between known 2D coordinates and detected 2D points
    # Assuming the first four points correspond to known_2d_coords
    corresponding_points = points[:len(known_2d_coords)]
    _, homography = cv2.findHomography(known_2d_coords, corresponding_points)

    # Compute 3D coordinates for the detected points
    points_3d = []
    for pt in points:
        pt_homogeneous = np.append(pt, 1)
        world_coord = np.dot(np.linalg.inv(homography), pt_homogeneous)
        world_coord /= world_coord[-1]
        points_3d.append(world_coord[:3])

    return np.array(points_3d)


def analyze_deformation(coords1, coords2):
    # 计算两组 3D 坐标之间的变形
    deformation = np.linalg.norm(coords1 - coords2, axis=1)
    return deformation


def main():
    # 加载不同时间点的两张图片
    img1 = cv2.imread('./ArucoShot/IMG_20230425_171500.jpg',
                      cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('./ArucoShot/IMG_20230426_110858.jpg',
                      cv2.IMREAD_GRAYSCALE)

    # 在两个图像中找到对应点
    points1, points2 = find_corresponding_points(img1, img2)

    # 四个点的已知 3D 世界坐标和 2D 像素坐标
    known_3d_coords = np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
                                [50, 50, 0]])
    known_2d_coords = np.array([[327.0, 462.75], [329.5, 431.0], [366.25, 463.0],
                                [366.75, 432.0]])

    # 相机矩阵（内参）
    camera_matrix = np.array([[596.34925072, 0, 400.35710334], [
        0, 596.49697012, 300.47081541], [0, 0, 1]])

    # 计算对应点的 3D 坐标
    coords1 = compute_3d_coordinates(
        points1, known_3d_coords, known_2d_coords, camera_matrix)
    coords2 = compute_3d_coordinates(
        points2, known_3d_coords, known_2d_coords, camera_matrix)

    # 分析两组3D坐标之间的变形
    deformation = analyze_deformation(coords1, coords2)
    print('Deformation:', deformation)


if __name__ == "__main__":
    main()
