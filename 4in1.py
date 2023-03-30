import sys
import cv2
import math
import argparse
import numpy as np
import pandas as pd
from scipy import spatial
import cv2.aruco as aruco


file = './data/IMG_2575.jpg'
npz = './calibration/result/Camera parameters.npz'
targetMarker = [0,1]
groupnum = 4


# 定义 OpenCV 支持的每个可能的 ArUco 标签的名称
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# 计算两个点之间的距离
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


# 找到距离最远的两个点
def find_furthest_points(points):
    max_dist = 0
    furthest_points = None
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dist = distance(points[i], points[j])
            if dist > max_dist:
                max_dist = dist
                furthest_points = (points[i], points[j])
    return furthest_points


# 计算两个点的平均坐标
def average_point(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]


points = [[1.2, 2.4], [3, 4], [5, 6]]   
furthest_points = find_furthest_points(points)
avg_point = average_point(furthest_points[0], furthest_points[1])
print("最远的两个点：", furthest_points)
print("它们的平均坐标：", avg_point[0],avg_point[1])



# 摄像头调用
cap = cv2.VideoCapture(0)
para = cv2.aruco.DetectorParameters_create()
para.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_APRILTAG

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(img_gray, aruco.Dictionary_get(aruco.DICT_6X6_250), parameters=para)
    aruco.drawDetectedMarkers(img_gray, corners)  # 在标记周围画一个正方形

    id_coord = {}
    if corners:
        for i, marker_corners in zip(range(len(ids)), corners):  # 遍历探测到的marker ID
            cv2.polylines(
                frame, [marker_corners.astype(int)], True, (0, 255, 255), 4, cv2.LINE_AA
            )
            markerIDThisIterate = ids[i][0]
            if markerIDThisIterate in targetMarker:  # 如果是目标marker的ID
            # 获得当前处理的marker在targetMarker中的下标，用于填充targetsWorldPoint
                targetIndex = targetMarker.index(markerIDThisIterate)
            else:
                continue
        
        # 计算每个marker中心的图像坐标
            markerCenter = corners[i][0].sum(0) / 4.0
            id_coord[str(ids[i][0]) + '_' + str(i + 1)] = markerCenter  # 储存至一个字典里方便后面调取

        for i in targetMarker:
            res = {key: val for key, val in id_coord.items() if key.startswith(str(i))}
            if len(res) == groupnum:  # 设定四个为一组

                center = sum(list(res.values())) / len(list(res.values()))  # 计算四个中心点的中心点
                image = cv2.circle(frame, (int(center[0]), int(center[1])), radius=10, color=(0, 0, 255), thickness=-1)
                vector = np.vectorize(np.int_)
                cv2.putText(
                image,
                f"id: {i}; Coordinate: {center[0], center[1]}",
                vector(center + 20),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
                #写入excel
                df = pd.DataFrame([center], columns=['x','y'])
                df.to_csv('../results/4in1.csv', mode='a', index=False, header=None)


            elif 2 < len(res) < groupnum:
                # 获取最远坐标点
                furthest_points = find_furthest_points(list(res.values()))
                avg_point = sum(furthest_points)/len(furthest_points)


                image = cv2.circle(frame, (int(avg_point[0]), int(avg_point[1])), radius=10, color=(0, 0, 255), thickness=-1)
                vector = np.vectorize(np.int_)
                cv2.putText(
                    frame,
                    f"id: {i}; Coordinate: {avg_point[0], avg_point[1]}",
                    vector(avg_point + 20),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )


            else:
                continue
    
    #显示输出帧
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    # 按下‘q’键，中断循环
    if key == ord("q"):
        break


#释放资源
cap.release()
cv2.destroyAllWindows()