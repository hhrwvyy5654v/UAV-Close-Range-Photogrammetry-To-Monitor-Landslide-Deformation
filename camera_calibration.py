"""_通过张正友标定法获取相机参数_
"""
# 导包
import os
import cv2
import numpy as np


# 图片在文件夹的位置
file_in = './calibration_plate/original/'   # 原始图片存放位置
file_mid = './calibration_plate/resize/'   # 更改大小图片存放位置
file_out = './calibration_plate/final/'   # 最后图片的保存位置


# 棋盘格模板规格,只算内角点个数,不算最外面的一圈点
width = 11
height = 8


def ResizeImage(filein, fileout, width, height):
    """_调整图片大小,防止图片过大引起崩溃_

    Args:
        filein (_string_): _输入图片的文件夹路径_
        fileout (_string_): _输出图片的文件夹路径_
        width (_int_): _输出图片宽度_
        height (_int_): _输出图片高度_
    """
    allImages = os.listdir(filein)
    for fname in allImages:
        image = cv2.imread(file_in + fname)
        out = cv2.resize(image, (width, height))
        cv2.imwrite(file_mid + fname, out)


# 更改图片尺寸
resize_width = 1704
resize_height = 1280
# ResizeImage(file_in, file_mid, resize_width, resize_height)


# 寻找棋盘格角点
world_point = np.zeros((width * height, 3), np.float32)   # 初始化一个大小为width*height*3的0矩阵
world_point[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)   # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
world_points = []  # 世界坐标系中的三维点
image_points = []  # 图像平面的二维点

"""
角点精准化迭代过程的终止条件:
第一项:表示迭代次数达到最大次数时停止迭代;
第二项:表示角点位置变化的最小值已经达到最小时停止迭代;
第三项和第四项：表示设置寻找亚像素角点的参数,2
采用的停止准则是最大循环次数30和最大误差容限0.001
"""
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            30, 0.001)  


images = os.listdir(file_mid)   # 读入图像序列
index = 0

for fname in images:
    image = cv2.imread(file_mid + '/' + fname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   # RGB转灰度
    # 寻找棋盘格角点,存放角点于corners中
    # 如果找到足够点对,将其存储起来,ret为非零值
    ret, corners = cv2.findChessboardCorners(gray, (width, height), None)
    # 检测到角点后,进行亚像素级别角点检测,更新角点
    if ret == True:
        index += 1
        # 输入图像gray;角点初始坐标corners;搜索窗口为2*winsize+1;表示窗口的最小(-1.-1)表示忽略;求角点的迭代终止条件
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        world_points.append(world_point)   # 空间坐标
        image_points.append(corners)  # 角点坐标即图像坐标
        # 角点显示
        cv2.drawChessboardCorners(image, (width, height), corners, ret)
        cv2.imshow('角点显示', image)
        cv2.imwrite(file_out + '/Corners_' + str(index) + '.jpg', image)
        cv2.waitKey(10)

cv2.destroyAllWindows()



"""
求解参数
输入:世界坐标系里的位置;像素坐标;图像的像素尺寸大小;
输出:
    ret: 重投影误差;
    mtx:内参矩阵;
    dist:畸变系数;
    rvecs:旋转向量 (外参数);
    tvecs:平移向量 (外参数);
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    world_points, image_points, gray.shape[::-1], None, None)


"""
优化内参数和畸变系数
使用相机内参mtx和畸变系数dist,并使用cv2.getOptimalNewCameraMatrix()去除畸变矫正后图像四周黑色的区域
通过设定自由自由比例因子alpha:
    当alpha设为0的时候,将会返回一个剪裁过的将去畸变后不想要的像素去掉的内参数和畸变系数;
    当alpha设为1的时候,将会返回一系个包含额外黑色像素点的内参数和畸变数,并返回一个ROI用于将其剪裁掉。
"""
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
    mtx, dist, (resize_width, resize_height), 0, (resize_width, resize_height))
print("ret(重投影误差):", ret,
        "\n\nmtx(内参矩阵):\n", mtx,
        "\n\ndist(畸变参数):\n", dist,  # 5个畸变参数,(k_1,k_2,p_1,p_2,k_3)
        "\n\nrvecs(旋转向量):\n", rvecs,
        "\n\ntvecs(平移向量):\n", tvecs
        )

# 保存相机参数(内参矩阵、畸变参数、旋转向量、平移向量)
np.savez('./camera_parameters/IMX686.npz', mtx=mtx, dist=dist,
         rvecs=rvecs, tvecs=tvecs)  # 分别使用mtx,dist,rvecs,tvecs命名数组