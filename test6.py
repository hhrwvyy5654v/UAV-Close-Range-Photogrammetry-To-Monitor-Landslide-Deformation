import cv2
import numpy as np
import itertools

def estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs):
    _, rvec, tvec, _ = cv2.solvePnPRansac(world_coords, pixel_coords, camera_matrix, dist_coeffs)
    return rvec, tvec

def triangulate_points(pixel_coords1, pixel_coords2, camera_matrix, rvec1, tvec1, rvec2, tvec2):
    proj_matrix1 = np.dot(camera_matrix, np.hstack((cv2.Rodrigues(rvec1)[0], tvec1)))
    proj_matrix2 = np.dot(camera_matrix, np.hstack((cv2.Rodrigues(rvec2)[0], tvec2)))
    world_coords = cv2.triangulatePoints(proj_matrix1, proj_matrix2, pixel_coords1.T, pixel_coords2.T).T
    world_coords = (world_coords / world_coords[:, 3:])[:, :3]
    return world_coords

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
camera_matrix = np.array([[596.34925072, 0, 400.35710334], [0, 596.49697012, 300.47081541], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.array([9.86732100e-02,-4.94565440e-01,-4.51708736e-04,2.89052555e-04,8.22459145e-01], dtype=np.float32).reshape(5, 1)

# 计算四幅图像的相机姿态
camera_poses = [estimate_camera_pose(world_coords, pixel_coords, camera_matrix, dist_coeffs) for world_coords, pixel_coords in zip(world_coords_list, pixel_coords_list)]

# 示例：将图像1上的像素坐标 (100, 100) 转换为世界坐标
pixel_coord_example = (403.75 , 433.0)
pixel_coords = np.array([pixel_coord_example], dtype=np.float32)

# 两两图像组合进行三角测量
triangulated_points = []
for (i, j) in itertools.combinations(range(len(camera_poses)), 2):
    rvec1, tvec1 = camera_poses[i]
    rvec2, tvec2 = camera_poses[j]
    world_coord = triangulate_points(pixel_coords, pixel_coords, camera_matrix, rvec1, tvec1, rvec2, tvec2)[0]
    triangulated_points.append(world_coord)

# 对结果取平均值
world_coord_example = np.mean(triangulated_points, axis=0)
print(f"Pixel coordinate {pixel_coord_example} in the four images corresponds to world coordinate {world_coord_example}")
