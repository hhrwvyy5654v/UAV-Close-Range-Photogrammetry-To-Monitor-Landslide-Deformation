"""_通过张正友标定法获取相机参数_
"""
# 导包
import os
import cv2
import numpy as np

# 定义棋盘格模板规格:只算内角点个数,不算最外面的一圈点
pattern_size = (11, 8)
# 定义每个棋盘格的物理尺寸（单位：毫米）
square_size = 40.0


# 图像所在文件夹的位置
original_images = './CalibrationPlate/original/'   # 原始图片保存位置
resize_images = './CalibrationPlate/resize/'   # 调整尺寸后的图像保存位置
corner_images = './CalibrationPlate/corner/'   # 显示角点的图像保存位置


def ResizeImage(input, output, width, height):
    """_调整图片大小,防止图片过大引起崩溃_
    Args:
        input (_string_): _输入图片的文件夹路径_
        output (_string_): _输出图片的文件夹路径_
        width (_int_): _输出图片宽度_
        height (_int_): _输出图片高度_
    """
    Images = os.listdir(input)
    for fname in Images:
        image = cv2.imread(input + fname)
        out = cv2.resize(image, (width, height))
        cv2.imwrite(output + fname, out)


# 更改图片尺寸
new_width = 800
new_height = 600
ResizeImage(original_images, resize_images, new_width, new_height)


# 世界坐标系中的棋盘格点,例如(0,0,0),(2,0,0)...(8,5,0)，去掉Z坐标，记为二维矩阵
world_point = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
# 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
world_point[:, :2] = np.mgrid[0:pattern_size[0]*square_size:square_size,
                              0:pattern_size[1]*square_size:square_size].T.reshape(-1, 2)
# 储存棋盘格角点的世界坐标和图像坐标对
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


images = os.listdir(resize_images)   # 读入图像序列
index = 0

for fname in images:
    image = cv2.imread(resize_images + '/' + fname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   # RGB转灰度
    # 寻找棋盘格角点,存放角点于corners中
    # 如果找到足够点对,将其存储起来,ret为非零值
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
    # 检测到角点后,进行亚像素级别角点检测,更新角点

    if ret == True:
        index += 1
        # 输入图像gray;角点初始坐标corners;搜索窗口为2*winsize+1;表示窗口的最小(-1.-1)表示忽略;求角点的迭代终止条件
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        world_points.append(world_point)   # 世界坐标
        image_points.append(corners)  # 图像坐标
        cv2.drawChessboardCorners(image, pattern_size, corners, ret)
        cv2.imwrite(corner_images + '/corners_' + str(index) + '.jpg', image)
        cv2.waitKey(10)

cv2.destroyAllWindows()


"""
求解参数
输入:世界坐标系里的位置;像素坐标;图像的像素尺寸大小;
输出:
    ret: 重投影误差;
    mtx: 内参矩阵;
    dist: 畸变系数;
    rvecs: 旋转向量 (外参数);
    tvecs: 平移向量 (外参数);
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    world_points, image_points, gray.shape[::-1], None, None)

# 保存相机参数(内参矩阵、畸变参数、旋转向量、平移向量)
np.savez('./Parameter/豪威OV48B.npz', mtx=mtx, dist=dist,
         rvecs=rvecs, tvecs=tvecs)  # 分别使用mtx,dist,rvecs,tvecs命名数组

print("ret(重投影误差):", ret,
      "\n\nmtx(内参矩阵):\n", mtx,
      "\n\ndist(畸变参数):\n", dist,  # 5个畸变参数,(k1,k2,p1,p2,k3)
      "\n\nrvecs(旋转向量):\n", rvecs,
      "\n\ntvecs(平移向量):\n", tvecs
      )

# # cv2.Rodrigues()函数用于将旋转向量转换为旋转矩阵
# R, jacobian = cv2.Rodrigues(rvecs[0])
# print("\n旋转矩阵[0]:\n", R)

# R, jacobian = cv2.Rodrigues(rvecs[1])
# print("\n旋转矩阵[1]:\n", R)
