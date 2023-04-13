import cv2
import numpy as np
import math

# 四个特征点的世界坐标,单位是毫米
object_3d_points = np.array(([-50, -50, 0],
                            [-50, 50, 0],
                            [50, -50, 0],
                            [50, 50, 0]), dtype=np.double)

# 四个特征点在图像上的对应点坐标
object_2d_points = np.array(([331.5, 977.5],
                            [326.75, 456.75],
                            [849.5, 974.0],
                            [847.75, 455.75]), dtype=np.double)
# 内参矩阵
camera_matrix = np.array(([1.26843647e+03, 0, 8.55216528e+02],
                         [0, 1.26953172e+03, 6.38366415e+02],
                         [0, 0, 1.0]), dtype=np.double)
# 畸变系数
dist_coefs = np.array([7.17124268e-02, -1.75341815e-01, -
                      8.06138780e-04, 9.80389409e-05, 1.99290630e-01], dtype=np.double)

# 求解相机位姿
found, rvec, tvec = cv2.solvePnP(
    object_3d_points, object_2d_points, camera_matrix, dist_coefs)
rotM = cv2.Rodrigues(rvec)[0]
camera_postion = -np.matrix(rotM).T * np.matrix(tvec)
print("相机位姿:", camera_postion.T)


# 计算相机坐标系的三轴旋转欧拉角，旋转后可以转出世界坐标系。旋转顺序z,y,x
thetaZ = math.atan2(rotM[1, 0], rotM[0, 0])*180.0/math.pi
thetaY = math.atan2(-1.0*rotM[2, 0], math.sqrt(rotM[2, 1]
                    ** 2 + rotM[2, 2]**2))*180.0/math.pi
thetaX = math.atan2(rotM[2, 1], rotM[2, 2])*180.0/math.pi

# 相机坐标系下值
x = tvec[0]
y = tvec[1]
z = tvec[2]
# 进行三次旋转


def RotateByZ(Cx, Cy, thetaZ):
    rz = thetaZ*math.pi/180.0
    outX = math.cos(rz)*Cx - math.sin(rz)*Cy
    outY = math.sin(rz)*Cx + math.cos(rz)*Cy
    return outX, outY


def RotateByY(Cx, Cz, thetaY):
    ry = thetaY*math.pi/180.0
    outZ = math.cos(ry)*Cz - math.sin(ry)*Cx
    outX = math.sin(ry)*Cz + math.cos(ry)*Cx
    return outX, outZ


def RotateByX(Cy, Cz, thetaX):
    rx = thetaX*math.pi/180.0
    outY = math.cos(rx)*Cy - math.sin(rx)*Cz
    outZ = math.sin(rx)*Cy + math.cos(rx)*Cz
    return outY, outZ


(x, y) = RotateByZ(x, y, -1.0*thetaZ)
(x, z) = RotateByY(x, z, -1.0*thetaY)
(y, z) = RotateByX(y, z, -1.0*thetaX)
Cx = x*-1
Cy = y*-1
Cz = z*-1

print("相机位置:", Cx, Cy, Cz)
print("相机旋转角:", thetaX, thetaY, thetaZ)

# 对第五个点进行验证
Out_matrix = np.concatenate((rotM, tvec), axis=1)
pixel = np.dot(camera_matrix, Out_matrix)
pixel1 = np.dot(pixel, np.array([150, 50, 0, 1], dtype=np.double))
pixel2 = pixel1/pixel1[2]
print("第五个点的像素坐标:", pixel2)
