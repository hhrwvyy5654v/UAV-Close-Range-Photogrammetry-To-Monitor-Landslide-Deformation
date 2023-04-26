import cv2
import numpy as np

"""_像素坐标到相机坐标的转换_
"""

# 定义相机矩阵和畸变系数
mtx = np.array([[596.34925072, 0.0,          400.35710334],
                [0.0,          596.49697012, 300.47081541],
                [0.0,          0.0,          1.0]])
dist = np.array([[9.86732100e-02, -4.94565440e-01, -
                4.51708734e-04, 2.89052556e-04, 8.22459145e-01]])


# 定义像素坐标
img_point = np.array([[306.5,481.75],[290.0,456.0]], dtype=np.float32)

# 像素坐标转换为相机坐标
cam_point = cv2.undistortPoints(img_point, mtx, dist)

print("相机坐标:\n", cam_point)
