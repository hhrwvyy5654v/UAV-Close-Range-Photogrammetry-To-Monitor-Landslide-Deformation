import cv2
import numpy as np


def estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs):
    # 使用PnP算法估计相机姿态
    _, rvec, tvec, _ = cv2.solvePnPRansac(
        world_coords, pixel_coords, camera_matrix, dist_coeffs)
    return rvec, tvec


def pixel_to_world(pixel_coord, camera_matrix, rvec, tvec, z_world=0):
    # 将像素坐标转换为世界坐标
    pixel_coord = np.array([*pixel_coord, 1], dtype=np.float32)
    inv_camera_matrix = np.linalg.inv(camera_matrix)
    uv_point = np.dot(inv_camera_matrix, pixel_coord)

    rot_matrix, _ = cv2.Rodrigues(rvec)
    inv_rot_matrix = np.linalg.inv(rot_matrix)

    tvec = tvec.reshape(3, 1)
    world_coord = np.dot(inv_rot_matrix, (z_world * uv_point - tvec))
    return world_coord


# 四幅图像的世界坐标和像素坐标
world_coords_list = [
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32),
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32),
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32),
    np.array([[-50, -50, 0], [-50, 50, 0], [50, -50, 0],
             [50, 50, 0]], dtype=np.float32)
]

pixel_coords_list = [
    np.array([[327.0, 462.75], [329.5, 431.0], [366.25, 463.0],
             [366.75, 432.0]], dtype=np.float32),
    np.array([[368.25, 481.0], [371.5, 447.25], [
             411.0, 484.0], [412.0, 450.0]], dtype=np.float32),
    np.array([[467.75, 417.5], [464.0, 385.75], [507.5, 420.5],
             [502.25, 388.75]], dtype=np.float32),
    np.array([[507.75, 400.25], [497.5, 370.0], [
             547.0, 398.0], [535.0, 368.0]], dtype=np.float32)
]

# 相机内参矩阵和畸变系数（需要根据实际相机参数进行替换）
camera_matrix = np.array([[596.34925072, 0, 400.35710334], [
                         0, 596.49697012, 300.47081541], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.array([9.86732100e-02,-4.94565440e-01,-4.51708736e-04,2.89052555e-04,8.22459145e-01], dtype=np.float32).reshape(5, 1)

# 计算每幅图像的相机姿态
camera_poses = [estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs)
                for world_coords, pixel_coords in zip(world_coords_list, pixel_coords_list)]

# 示例：将图像1上的像素坐标转换为世界坐标
pixel_coord_example = (403.75 , 433.0)
rvec, tvec = camera_poses[0]
world_coord_example = pixel_to_world(
    pixel_coord_example, camera_matrix, rvec, tvec)
print(f"Pixel coordinate {pixel_coord_example} in image 1 corresponds to world coordinate {world_coord_example}")
