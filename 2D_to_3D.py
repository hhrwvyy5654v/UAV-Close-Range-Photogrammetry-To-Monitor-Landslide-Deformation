import numpy as np
import cv2

camera_parameter = {
    # R:旋转矩阵
    "R": [[ 0.99842466,-0.00670601,-0.05570656],
        [0.00938999,0.99880033,0.04805963],
        [0.05531744,-0.048507,0.99728985]],
    # T：平移向量
    "T": [-204.38036057,-143.87274813,458.71932771],
    # 焦距:f/dx, f/dy
    "f": [596.34925072,596.49697012],
    # 主点:主轴与像平面的交点
    "c": [400.35710334, 300.47081541]
}


def pixel_to_world(camera_intrinsics, r, t, img_points):
    K_inv = camera_intrinsics.I
    R_inv = np.asmatrix(r).I
    R_inv_T = np.dot(R_inv, np.asmatrix(t))
    world_points = []
    coords = np.zeros((3, 1), dtype=np.float64)
    for img_point in img_points:
        coords[0] = img_point[0]
        coords[1] = img_point[1]
        coords[2] = 1.0
        cam_point = np.dot(K_inv, coords)
        cam_R_inv = np.dot(R_inv, cam_point)
        scale = R_inv_T[2][0] / cam_R_inv[2][0]
        scale_world = np.multiply(scale, cam_R_inv)
        world_point = np.asmatrix(scale_world) - np.asmatrix(R_inv_T)
        pt = np.zeros((3, 1), dtype=np.float64)
        pt[0] = world_point[0]
        pt[1] = world_point[1]
        pt[2] = 0
        world_points.append(pt.T.tolist())

    return world_points


if __name__ == '__main__':
    f = camera_parameter["f"]
    c = camera_parameter["c"]
    camera_intrinsic = np.mat(np.zeros((3, 3), dtype=np.float64))
    camera_intrinsic[0, 0] = f[0]
    camera_intrinsic[1, 1] = f[1]
    camera_intrinsic[0, 2] = c[0]
    camera_intrinsic[1, 2] = c[1]
    camera_intrinsic[2, 2] = np.float64(1)
    r = camera_parameter["R"]
    t = np.asmatrix(camera_parameter["T"]).T

    img_points = np.array(([290.0 , 456.0],
                           [306.5 , 481.75]), dtype=np.double)
    result = pixel_to_world(camera_intrinsic, r, t, img_points)
    print('对应的世界坐标为：')
    print(result)
