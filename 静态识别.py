import numpy as np
import time
import cv2
import cv2.aruco as aruco

#读取图片
frame=cv2.imread('./aruco_images/IMG_2575.jpg')
#调整图片大小
frame=cv2.resize(frame,None,fx=0.2,fy=0.2,interpolation=cv2.INTER_CUBIC)
#灰度话
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#设置预定义的字典
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
#使用默认值初始化检测器参数
parameters =  aruco.DetectorParameters_create()
#使用aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

"""
corners:检测到的aruco标记的角点列表,对于每个标记,其四个角点均按其原始顺序返回（从右上角开始顺时针旋转）,第一个角是右上角,然后是右下角,左下角和左上角。
ids:检测到的每个标记的 id,需要注意的是第三个参数和第四个参数具有相同的大小；
rejectedImgPoints:抛弃的候选标记列表,即检测到的、但未提供有效编码的正方形。每个候选标记也由其四个角定义,其格式与第三个参数相同,该参数若无特殊要求可以省略。
"""

print("corners:\n",corners)
#print("\nids:\n",ids)
#print("\nrejectedImgPoints:\n",rejectedImgPoints)

#画出标志位置
aruco.drawDetectedMarkers(frame, corners,ids)


cv2.imshow("frame",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
