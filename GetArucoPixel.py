'''
Description: 获取aruco码的中心点的像素坐标
FilePath: \GetArucoPixel.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-05-03 18:37:15
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-14 10:25:49
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import os
import cv2
import csv
import numpy as np

# 指定文件夹路径
folder_path = "./ArucoShot/800x600/"
# 指定保存Aruco码中心点像素坐标的csv文件
csv_name = './ArucoShot/PixelCoordinates.csv'
# 使用默认值初始化检测器参数
parameters = cv2.aruco.DetectorParameters_create()
# 指定Aruco的字典参数
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)


# 写入csv文件时先清空其全部内容:使用w模式打开文件，然后再写入新的内容
with open(csv_name, mode="w", newline="", encoding="utf-8") as file:
    # 创建一个csv.writer对象来写入CSV格式数据
    writer = csv.writer(file)
    # 使用writerow()方法写入表头行
    writer.writerow(["ImageName", "ArucoId", "X", "Y"])
    # 遍历文件夹下的所有文件
    for filename in os.listdir(folder_path):
        # 判断文件是否为图片文件
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # 使用OpenCV读取图片
            image = cv2.imread(os.path.join(folder_path, filename))
            # 检测图像中的标记
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
                image, dictionary, parameters=parameters)
            if ids is not None:
                print("\n在图像", filename, "中共检测出", len(ids), "个arUco码")
                # 计算每个标记的中心点
                for i in range(len(corners)):
                    # 获取当前标记的角
                    markerCorners = corners[i][0]
                    # 计算当前标记的中心点
                    center = np.mean(markerCorners, axis=0)
                    # 将坐标信息保存为列表
                    coordinate = [str(filename), int(
                        ids[i]), center[0], center[1]]
                    # 创建一个csv.writer对象来写入CSV格式数据
                    writer = csv.writer(file)
                    # 写入数据
                    writer.writerow(coordinate)
                    # 打印输出
                    print("coordinate:", coordinate)
            else:
                print("\n在图像", filename, "中未检测出ArUco码")
