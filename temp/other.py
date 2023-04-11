
# 矫正畸变
image2 = cv2.imread(file_mid + '/IMG_2578.jpg')
dst = cv2.undistort(image2, mtx, dist, None, newcameramtx)
cv2.imwrite(file_out + '/calibresult.jpg', dst)
print("\n\nnewcameramtx(优化后相机内参):\n", newcameramtx)

# 反投影误差total_error,越接近0,说明结果越理想。
total_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(
        objpoints[i], rvecs[i], tvecs[i], mtx, dist)   # 计算三维点到二维图像的投影
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / \
        len(imgpoints2)   # 反投影得到的点与图像上检测到的点的误差
    total_error += error
print(("\n\ntotal error:"), total_error / len(objpoints))   # 记平均