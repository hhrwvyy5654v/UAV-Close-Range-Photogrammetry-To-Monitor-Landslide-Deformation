import os
import cv2
import numpy as np


"""_标定相机_"""
def calibrate_camera(image_points, object_points, image_size):
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, image_size, None, None)
    # 计算重投影误差
    mean_error = 0
    for i in range(len(object_points)):
        imgpoints2, _ = cv2.projectPoints(object_points[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(image_points[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
    print("total error: ", mean_error / len(object_points))
    return mtx, dist


"""_获取角点_"""
def get_image_points(images):
    image_points = []
    for image in images:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
        if ret:
            image_points.append(corners)
    return image_points

"""_获取物体坐标系中的坐标_"""
def get_object_points(images):
    object_points = []
    for i in range(len(images)):
        object_point = np.zeros((6 * 9, 3), np.float32)
        object_point[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
        object_point[:, 2] = 0
        object_points.append(object_point)
    return object_points

if __name__ == '__main__':
    path="./calibration/original image/"
    files = os.listdir(path) 
    nums=len(files)
    images = []
    for i in range(1, nums):
        filename = path+files[i]
        image = cv2.imread(filename)
        images.append(image)
        
    image_size = (images[0].shape[1], images[0].shape[0])
    print("image_size:",image_size)
    image_points = get_image_points(images)
    object_points = get_object_points(images)

    mtx, dist = calibrate_camera(image_points, object_points, image_size)
    print("mtx:",mtx,"\ndist:",dist)