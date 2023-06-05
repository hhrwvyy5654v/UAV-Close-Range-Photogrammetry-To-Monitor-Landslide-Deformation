'''
Description: 
FilePath: \ArucoToWord.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-05-15 20:48:08
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-05-17 09:32:33
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''

import cv2
import numpy as np
from docx import Document
from docx.shared import Inches

# 创建Aruco码


def create_aruco_markers(rows, cols, aruco_dict, marker_length, marker_separation, marker_ids):
    aruco_params = cv2.aruco.DetectorParameters_create()

    # 创建3D对象点数组
    obj_points = np.zeros((4, 3), dtype=np.float32)
    obj_points[:, :2] = np.array([[0, 0], [marker_length, 0], [
                                 marker_length, marker_length], [0, marker_length]])
    obj_points_array = [obj_points] * (rows * cols)

    aruco_board = cv2.aruco.Board_create(objPoints=obj_points_array,
                                         dictionary=aruco_dict,
                                         ids=marker_ids)
    img_size = (cols * (marker_length + marker_separation) + marker_separation,
                rows * (marker_length + marker_separation) + marker_separation)
    aruco_image = np.full(img_size, 255, dtype=np.uint8)
    for i, obj_points in enumerate(aruco_board.objPoints):
        marker_image = cv2.aruco.drawMarker(
            aruco_dict, marker_ids[i][0], marker_length)
        x = marker_separation + (i % cols) * \
            (marker_length + marker_separation)
        y = marker_separation + (i // cols) * \
            (marker_length + marker_separation)
        aruco_image[y:y + marker_length, x:x + marker_length] = marker_image
    return aruco_image

# 保存Aruco码到Word文件


def save_aruco_markers_to_word(doc, aruco_image, image_name):
    cv2.imwrite(image_name, aruco_image)
    doc.add_picture(image_name, width=Inches(8.27), height=Inches(11.69))
    doc.save('aruco_markers.docx')


# 参数设置
rows = 2
cols = 3
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
marker_length = 50  # 单位：毫米
marker_separation = 50  # 单位：毫米
marker_ids = np.array([[0], [1], [2], [3], [4], [5]]).reshape(rows, cols)

# 将毫米转换为像素
dpi = 96  # 假设每英寸96像素
marker_length_pixels = int(marker_length * dpi / 25.4)
marker_se_pixels = int(marker_separation * dpi / 25.4)

# 生成Aruco码
aruco_image = create_aruco_markers(
    rows, cols, aruco_dict, marker_length_pixels, marker_separation_pixels, marker_ids)

# 保存Aruco码到Word文件
doc = Document()
save_aruco_markers_to_word(doc, aruco_image, 'aruco_markers.png')
