"""根据两幅图像,在已知P1,P2,P3,P4四点对应的世界坐标和像素坐标的情况下,计算出其它点的世界坐标_
"""
import os
import re
import cv2
import csv
import math
import time
import random
import argparse
import threading
import subprocess
import numpy as np
from PIL import Image, ImageTk
PI=math.pi
RoundAngle=180.0


class PNP_Solver():
    def __init__(self):
        self.Points3D = np.zeros((1, 4, 3), np.float32)  # 存放4组世界坐标位置
        self.Points2D = np.zeros((1, 4, 2), np.float32)  # 存放4组像素坐标位置
        self.point2find = np.zeros((1, 2), np.float32)
        self.cameraMatrix = None
        self.distCoefs = None
        self.f = 0

    # 旋转矢量转换为欧拉角
    def rotationVectorToEulerAngles(self, rvecs, anglestype):
        R = np.zeros((3, 3), dtype=np.float64)
        cv2.Rodrigues(rvecs, R)
        sy = math.sqrt(R[2, 1] * R[2, 1] + R[2, 2] * R[2, 2])
        singular = sy < 1e-6
        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0
        if anglestype == 0:
            x = x*RoundAngle/PI
            y = y*RoundAngle/PI
            z = z*RoundAngle/PI
        elif anglestype == 1:
            x = x
            y = y
            z = z
        return x, y, z

    # 第一次旋转:将空间点绕Z轴旋转
    def CodeRotateByZ(self, x,  y,  thetaz):
        x1 = x  # 将变量拷贝一次，保证&x == &outx这种情况下也能计算正确
        y1 = y
        rz = thetaz*PI/RoundAngle
        outx = math.cos(rz)*x1 - math.sin(rz)*y1
        outy = math.sin(rz)*x1 + math.cos(rz)*y1
        return outx, outy

    # 第二次旋转：将空间点绕Y轴旋转
    def CodeRotateByY(self, x, z, thetay):
        x1 = x
        z1 = z
        ry = thetay * PI / RoundAngle
        outx = math.cos(ry) * x1 + math.sin(ry) * z1
        outz = math.cos(ry) * z1 - math.sin(ry) * x1
        return outx, outz

    # 第三次旋转：将空间点绕X轴旋转
    def CodeRotateByX(self, y, z, thetax):
        y1 = y
        z1 = z
        rx = (thetax * PI) / RoundAngle
        outy = math.cos(rx) * y1 - math.sin(rx) * z1
        outz = math.cos(rx) * z1 + math.sin(rx) * y1
        return outy, outz

    def solver(self):
        retval, self.rvec, self.tvec = cv2.solvePnP(
            self.Points3D, self.Points2D, self.cameraMatrix, self.distCoefs)
        thetax, thetay, thetaz = self.rotationVectorToEulerAngles(self.rvec, 0)
        x = self.tvec[0][0]
        y = self.tvec[1][0]
        z = self.tvec[2][0]

        self.Position_OwInCx = x
        self.Position_OwInCy = y
        self.Position_OwInCz = z
        self.Position_theta = [thetax, thetay, thetaz]

        print('\nPosition_theta:',self.Position_theta)
        x, y = self.CodeRotateByZ(x, y, -1 * thetaz)
        x, z = self.CodeRotateByY(x, z, -1 * thetay)
        y, z = self.CodeRotateByX(y, z, -1 * thetax)

        self.Theta_W2C = ([-1*thetax, -1*thetay, -1*thetaz])
        self.Position_OcInWx = x*(-1)
        self.Position_OcInWy = y*(-1)
        self.Position_OcInWz = z*(-1)
        self.Position_OcInW = np.array(
            [self.Position_OcInWx, self.Position_OcInWy, self.Position_OcInWz])
        print('\nPosition_OcInW:', self.Position_OcInW)

    # 将像素坐标转换成世界坐标
    def WordFrame2ImageFrame(self, WorldPoints):
        pro_points, jacobian = cv2.projectPoints(WorldPoints, self.rvecs, self.tvecs, self.cameraMatrix, self.distCoefs)
        return pro_points

    def ImageFrame_To_CameraFrame(self, pixPoints):
        fx = self.cameraMatrix[0][0]
        u0 = self.cameraMatrix[0][2]
        fy = self.cameraMatrix[1][1]
        v0 = self.cameraMatrix[1][2]
        zc = (self.f[0]+self.f[1])/2
        xc = (pixPoints[0] - u0) * self.f[0] / fx  # f=fx*传感器尺寸/分辨率
        yc = (pixPoints[1] - v0) * self.f[1] / fy
        point = np.array([xc, yc, zc])
        return point

    # 读取标定文件中的相机内参
    def getudistmap(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            rows = [row for row in spamreader]
            self.cameraMatrix = np.zeros((3, 3))
            # 豪威OV48B的尺寸为1/2英寸，即靶面尺寸为宽6.4mm*高4.8mm
            size_w = 6.4
            size_h = 4.8
            imageWidth = int(rows[0][1])
            imageHeight = int(rows[0][2])
            self.cameraMatrix[0][0] = rows[1][1]
            self.cameraMatrix[1][1] = rows[1][2]
            self.cameraMatrix[0][2] = rows[1][3]
            self.cameraMatrix[1][2] = rows[1][4]
            self.cameraMatrix[2][2] = 1
            if len(rows[2]) == 5:
                self.distCoefs = np.zeros((4, 1))
                self.distCoefs[0][0] = rows[2][1]
                self.distCoefs[1][0] = rows[2][2]
                self.distCoefs[2][0] = rows[2][3]
                self.distCoefs[3][0] = rows[2][4]
                # K 的值是随图像尺寸缩放
                scaled_K = self.cameraMatrix * 0.8
                scaled_K[2][2] = 1.0
            else:
                self.distCoefs = np.zeros((1, 5))
                self.distCoefs[0][0] = rows[2][1]
                self.distCoefs[0][1] = rows[2][2]
                self.distCoefs[0][2] = rows[2][3]
                self.distCoefs[0][3] = rows[2][4]
                self.distCoefs[0][4] = rows[2][5]
                
            print('\n图像尺寸: %d*%d' % (imageWidth, imageHeight))   #影像尺寸(像素)
            print('\n内参矩阵: \n', self.cameraMatrix)  # 相机矩阵
            print('\n畸变系数: \n', self.distCoefs)    # 畸变系数
            self.f = [self.cameraMatrix[0][0] *
                      (size_w/imageWidth), self.cameraMatrix[1][1]*(size_h/imageHeight)]
            print('\nf=', self.f)
            return


class Get_Distance_Of_2lines_In_3D():
    """根据两幅图得到的两条直线,计算出P点的世界坐标_

        已经获得世界坐标系的相机构成的直线A和B,
        因此求出两条直线A和B的交点即可求出目标点的世界坐标,
        但是在现实世界中由于误差的存在,直线A和B基本不会相交,
        因此在计算时需要求它们二者之间的最近点。

    """

    def dot(self, ax, ay, az, bx, by, bz):
        result = ax*bx + ay*by + az*bz
        return result

    def cross(self, ax, ay, az, bx, by, bz):
        x = ay*bz - az*by
        y = az*bx - ax*bz
        z = ax*by - ay*bx
        return x, y, z

    def crossarray(self, a, b):
        x = a[1]*b[2] - a[2]*b[1]
        y = a[2]*b[0] - a[0]*b[2]
        z = a[0]*b[1] - a[1]*b[0]
        return np.array([x, y, z])

    def norm(self, ax, ay, az):
        return math.sqrt(self.dot(ax, ay, az, ax, ay, az))

    def norm2(self, one):
        return math.sqrt(np.dot(one, one))

    # 通过世界坐标系的相机坐标a1，P点坐标a2，构成第一条直线A
    def SetLineA(self, A1x, A1y, A1z, A2x, A2y, A2z):
        self.a1 = np.array([A1x, A1y, A1z])
        self.a2 = np.array([A2x, A2y, A2z])

    # 通过世界坐标系的相机坐标b1，P点坐标b2，构成第一条直线B
    def SetLineB(self, B1x, B1y, B1z, B2x, B2y, B2z):
        self.b1 = np.array([B1x, B1y, B1z])
        self.b2 = np.array([B2x, B2y, B2z])

    def GetDistance(self):
        d1 = self.a2 - self.a1
        d2 = self.b2 - self.b1
        e = self.b1 - self.a1

        cross_e_d2 = self.crossarray(e, d2)
        cross_e_d1 = self.crossarray(e, d1)
        cross_d1_d2 = self.crossarray(d1, d2)

        dd = self.norm2(cross_d1_d2)
        t1 = np.dot(cross_e_d2, cross_d1_d2)
        t2 = np.dot(cross_e_d1, cross_d1_d2)

        t1 = t1/(dd*dd)
        t2 = t2/(dd*dd)

        self.PonA = self.a1 + (self.a2 - self.a1) * t1
        self.PonB = self.b1 + (self.b2 - self.b1) * t2

        self.distance = self.norm2(self.PonB - self.PonA)
        print('\n距离:', self.distance)
        return self.distance


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('-file', type=str, default = 'calibration.csv')
    args = parser.parse_args()
    calibrationfile = args.file
    
    p4psolver1 = PNP_Solver()
    
    P11 = np.array([-50, -50, 0])
    P12 = np.array([-50, 50, 0])
    P13 = np.array([50, -50, 0])
    P14 = np.array([50, 50, 0]) 
    p11 = np.array([342.0 , 423.0])
    p12 = np.array([359.0 , 447.25])
    p13 = np.array([316.75 , 439.25])
    p14 = np.array([333.5 , 464.0]) 

    p4psolver1.Points3D[0] = np.array([P11,P12,P13,P14])
    p4psolver1.Points2D[0] = np.array([p11,p12,p13,p14])

    p4psolver1.point2find = np.array([306.5 , 481.75])
    p4psolver1.getudistmap(calibrationfile)
    p4psolver1.solver()



    p4psolver2 = PNP_Solver()
    P21 = np.array([-50, -50, 0])
    P22 = np.array([-50, 50, 0])
    P23 = np.array([50, -50, 0])
    P24 = np.array([50, 50, 0])
    
    p21 = np.array([415.0 , 417.0])
    p22 = np.array([436.0 , 437.5])
    p23 = np.array([394.0 , 436.5])
    p24 = np.array([415.0 , 457.0])

    p4psolver2.Points3D[0] = np.array([P21,P22,P23,P24])
    p4psolver2.Points2D[0] = np.array([p21,p22,p23,p24])
    p4psolver2.point2find = np.array([393.0,478.0])
    p4psolver2.getudistmap(calibrationfile)
    p4psolver2.solver()

    point2find1_CF = p4psolver1.ImageFrame_To_CameraFrame(p4psolver1.point2find)
    Oc1P_1 = np.array(point2find1_CF)
    print("\nOc1P_1:",Oc1P_1)

    Oc1P_1[0], Oc1P_1[1] = p4psolver1.CodeRotateByZ(Oc1P_1[0], Oc1P_1[1], p4psolver1.Theta_W2C[2])
    Oc1P_1[0], Oc1P_1[2] = p4psolver1.CodeRotateByY(Oc1P_1[0], Oc1P_1[2], p4psolver1.Theta_W2C[1])
    Oc1P_1[1], Oc1P_1[2] = p4psolver1.CodeRotateByX(Oc1P_1[1], Oc1P_1[2], p4psolver1.Theta_W2C[0])

    a1 = np.array([p4psolver1.Position_OcInWx, p4psolver1.Position_OcInWy, p4psolver1.Position_OcInWz])
    a2 =  a1 + Oc1P_1


    point2find2_CF = p4psolver2.ImageFrame_To_CameraFrame(p4psolver2.point2find)
    Oc2P_2 = np.array(point2find2_CF)
    print("\nOc1P_2:",Oc2P_2)

    Oc2P_2[0], Oc2P_2[1] = p4psolver2.CodeRotateByZ(Oc2P_2[0], Oc2P_2[1], p4psolver2.Theta_W2C[2])
    Oc2P_2[0], Oc2P_2[2] = p4psolver2.CodeRotateByY(Oc2P_2[0], Oc2P_2[2], p4psolver2.Theta_W2C[1])
    Oc2P_2[1], Oc2P_2[2] = p4psolver2.CodeRotateByX(Oc2P_2[1], Oc2P_2[2], p4psolver2.Theta_W2C[0])

    b1 = ([p4psolver2.Position_OcInWx, p4psolver2.Position_OcInWy, p4psolver2.Position_OcInWz])
    b2 = b1 + Oc2P_2
    
    g = Get_Distance_Of_2lines_In_3D()
    g.SetLineA(a1[0], a1[1], a1[2], a2[0], a2[1], a2[2])
    g.SetLineB(b1[0], b1[1], b1[2], b2[0], b2[1], b2[2])

    distance = g.GetDistance()

    pt = (g.PonA + g.PonB)/2

    print(pt)