"""_旋转向量转换为旋转矩阵_
"""
import numpy as np
import cv2 as cv
R_vec = np.array([[0.66104649], [-0.63066902], [-0.0488436]])
R_mat = cv.Rodrigues(R_vec)[0]
print(R_mat)