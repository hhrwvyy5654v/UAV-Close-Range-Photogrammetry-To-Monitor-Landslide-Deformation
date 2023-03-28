import numpy as np

class Camera(object):
    def __init__(self):
        # 左相机内参 及 畸变系数
        self.cam_matrix_left = np.array(
            [[1271.71, -0.1385, 376.5282], [0., 1270.87, 258.1373], [0., 0., 1.]])
        self.distortion_l = np.array(
            [[-0.5688, 5.9214, -0.00038018, -0.00052731, -61.7538]])
        # 右相机内参 及 畸变系数
        self.cam_matrix_right = np.array(
            [[1269.2524, -2.098026, 367.9874], [0., 1267.1973, 246.2712], [0., 0., 1.]])
        self.distortion_r = np.array(
            [[-0.5176, 2.4704, -0.0011, 0.0012, -16.1715]])
        # 右边相机相对于左边相机的 旋转矩阵 R ， 平移矩阵 T
        self.R = np.array([[1.0000, -0.0088, -0.0043],
                          [0.0088, 0.9999, 0.0072], [0.0042, -0.0072, 1.0000]])
        self.T = np.array([[-68.5321], [-0.5832], [-4.0933]])
        # 焦距
        self.focal_length = 6.00
        # 左右相机之间的距离 取 T 向量的第一维数值 单位 mm
        self.baseline = np.abs(self.T[0])
