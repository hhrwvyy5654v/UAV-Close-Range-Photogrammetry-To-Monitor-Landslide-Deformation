'''
Description: 根据两幅图像上对应的四个点的世界坐标系下的点坐标和相机坐标系下的像素坐标来求其他点的世界坐标
FilePath: \WorldBy2.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-05-03 18:37:15
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-14 10:45:46
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
# 导包
import cv2
import csv
import numpy as np


def estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs):
    # 使用PnP算法估计相机姿态
    _, rvec, tvec, _ = cv2.solvePnPRansac(
        world_coords, pixel_coords, camera_matrix, dist_coeffs)
    return rvec, tvec


def triangulate_points(pixel_coords1, pixel_coords2, camera_matrix, rvec1, tvec1, rvec2, tvec2):
    # 三角测量计算世界坐标
    proj_matrix1 = np.dot(camera_matrix, np.hstack(
        (cv2.Rodrigues(rvec1)[0], tvec1)))
    proj_matrix2 = np.dot(camera_matrix, np.hstack(
        (cv2.Rodrigues(rvec2)[0], tvec2)))
    world_coords = cv2.triangulatePoints(
        proj_matrix1, proj_matrix2, pixel_coords1.T, pixel_coords2.T).T
    world_coords = (world_coords / world_coords[:, 3:])[:, :3]
    return world_coords


# 两幅图像中对应的世界坐标和像素坐标
world_coords_list = [
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32),
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32)
]

# 两幅图像中的像素坐标
CSV_Name='./ArucoShot/PixelCoordinates.csv'
Image_A="IMG_20230425_171500.jpg"
Image_B="IMG_20230426_110858.jpg"

def Get_the_pixel_coordinates(csv_name,image_name):
    Pixel_coordinates = []
    with open(csv_name, 'r') as file:
        reader = csv.reader(file)
        next(reader) # 跳过第一行标题行
        for row in reader:
            if not row: # 检查该行是否为空
                continue
            if row[0]==image_name:
                aruco_id = int(row[1])
                x = float(row[2])
                y = float(row[3])
                Pixel_coordinates.append((aruco_id, [x, y]))
        Pixel_coordinates.sort(key=lambda x: x[0])
        Pixel_coordinates = [x[1] for x in Pixel_coordinates]
        return np.array(Pixel_coordinates[:-2], dtype=np.float32)

pixel_coords_list = [
    # 图像A的四个点对应的像素坐标
    Get_the_pixel_coordinates(CSV_Name,Image_A),
    # 图像B的四个点对应的像素坐标
    Get_the_pixel_coordinates(CSV_Name,Image_B)
]

# 加载npz文件读取相机的内参矩阵和畸变系数
data = np.load('./Parameter/13ProMax_9504x5344.npz')

# 获取mtx和dist参数
camera_matrix = data['mtx']
dist_coeffs = data['dist']

# 计算两幅图像的相机姿态
camera_poses = [estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs)
                for world_coords, pixel_coords in zip(world_coords_list, pixel_coords_list)]

# 获取每幅图像的旋转向量rvec和平移向量tvec
rvec1, tvec1 = camera_poses[0]
rvec2, tvec2 = camera_poses[1]


# 从csv文件中提取指定要求的坐标
def extract_data(csv_name: str,image_A,image_B,id):
    result = []
    with open(csv_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ImageName'] in [image_A, image_B] and row['ArucoId'] == id:
                result.append((float(row['X']), float(row['Y'])))
    return result

# 三角测量法将像素坐标转换为世界坐标
def pixel_to_world(pixel_coord):
    world_coord = triangulate_points(
        np.array([pixel_coord[0]], dtype=np.float32),
        np.array([pixel_coord[1]], dtype=np.float32),
        camera_matrix, rvec1, tvec1, rvec2, tvec2
    )[0]
    print(world_coord)
    return world_coord

# 传入不同的ArUco的id进行验证
CompareId4=pixel_to_world(extract_data(CSV_Name,Image_A,Image_B,'4'))  #id[4]
CompareId5=pixel_to_world(extract_data(CSV_Name,Image_A,Image_B,'5'))   #id[5]