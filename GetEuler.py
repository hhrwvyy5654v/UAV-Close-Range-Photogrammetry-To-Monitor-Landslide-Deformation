'''
Description: 以DJI Mavic 3M无人机为例,读取所拍摄照片的EXIF数据并提取欧拉角
FilePath: \GetEuler.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-06-12 15:00:23
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-12 15:00:35
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
from PIL import Image
import piexif

def get_euler_angles(image_path):
    # 打开图像文件
    img = Image.open(image_path)

    # 获取 EXIF 数据
    exif_data = piexif.load(img.info['exif'])

    # 提取欧拉角
    roll = exif_data['0th'][piexif.ImageIFD.RollAngle]
    pitch = exif_data['0th'][piexif.ImageIFD.PitchAngle]
    yaw = exif_data['0th'][piexif.ImageIFD.YawAngle]

    return roll, pitch, yaw

# 读取照片的欧拉角
image_path = './Drone/image.jpg'
roll, pitch, yaw = get_euler_angles(image_path)
print(f'Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}')
