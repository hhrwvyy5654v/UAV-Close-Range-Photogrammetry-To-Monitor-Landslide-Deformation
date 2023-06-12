# **<center>借助 Aruco 码定位对滑坡进行前后时间的三维测量</center>**

1. 项目目标：

   - 使用 Aruco 码作为参考点，对滑坡区域在不同时间点进行三维测量。
   - 分析滑坡区域的位移和变化，为滑坡监测和预警提供数据支持。

2. 设备和材料：

   - Aruco 码标记（可打印在耐候材料上，如塑料板）
   - 相机（具有固定焦距和已知内参矩阵的相机）
   - 三脚架或其他稳定的相机支架
   - 笔记本电脑或台式电脑（用于图像处理和分析）

3. 实施步骤：

   (1) 准备 Aruco 码：

      - 选择合适的 Aruco 字典（例如，cv2.aruco.DICT_6X6_250）。
      - 打印多个 Aruco 码，并将它们固定在耐候材料上。
      - 在滑坡区域放置 Aruco 码作为参考点。确保它们在前后时间的测量中都可见。

   (2) 图像采集：

      - 使用相同的相机参数（焦距、分辨率等）拍摄滑坡区域的照片。
      - 在不同时间点（例如，每周或每月）重复拍摄照片，以监测滑坡的变化。

   (3) 图像处理和分析：
      - 使用 OpenCV 检测 Aruco 码并估计相机姿态。
      - 使用相机姿态和内参矩阵计算每个 Aruco 码的三维坐标。
      - 对比前后时间的三维坐标，计算滑坡区域的位移。
      - 分析滑坡区域的变化趋势，为滑坡监测和预警提供数据支持。

4. 结果呈现：

   - 将滑坡区域的位移和变化可视化，例如，使用地图或三维模型展示。
   - 编写报告，总结滑坡监测结果和分析。
   - 提供滑坡预警建议，以降低滑坡对人员和设施的潜在风险。

5. 后续工作：
   - 定期更新滑坡监测数据，以持续跟踪滑坡的变化。
   - 根据监测结果调整预警策略，提高预警的准确性和及时性。
   - 探索其他监测方法（例如，无人机航拍、地质雷达等），以提高滑坡监测的精度和效率。


<br>

# **<center>无人机监测建筑沉降方案</center>**

1. 准备工作：

   - 在被测物旁放置标志物（如Aruco标记）和高精度全站仪。
   - 使用全站仪测量标志物的世界坐标系下的真实沉降数据。
   - 在目标建筑上放置监测标志物（如角反射器）。

2. 无人机拍摄：

    - 使用无人机拍摄目标建筑的可见光数据，确保参照点、监测标志物和角反射器清晰可见。

3. 计算机视觉处理：

   - 使用计算机视觉算法（如OpenCV）识别参照点、监测标志物和角反射器。
   - 利用三角化方法计算参考点坐标系下监测标志物和角反射器的三维坐标。

4. 沉降数据分析：

   - 对比多期监测标志物和角反射器的三维坐标，计算目标建筑的沉降数据。
   - 验证卫星监测结果的可靠性，通过对比沉降数据。
 
5. 实验验证：

   - 在博盈2号楼天台搭设试验场景。
   - 测试无人机在不同位置拍摄角反射器和标志物。
   - 利用算法识别参照物和角反射器，以参照物建立世界坐标系（X，Y，Z）。
   - 使用三角化方法计算角反射器在参照点坐标系下的三维坐标。
   - 通过计算多期角反射器坐标在各方向上的差值，实现角反射器位移监测。


![](Assets/无人机近景摄影测量监测滑坡形变.png)<br>

![](Assets/视频位移监测使用示意.jpg)<br>


## 参考文章

[计算机视觉对极几何之 Triangulate(三角化)](https://blog.csdn.net/u011178262/article/details/86729887)<br>
[关于 Aruco 标记的理解并对其进行姿态估计的可视化显示](https://blog.csdn.net/qq_45445740/article/details/122296313)<br>
[三角形法恢复空间点深度](https://blog.csdn.net/kokerf/article/details/72844455)<br>
[三角化特征点(triangulation)方法及实现对比](https://blog.csdn.net/weixin_41469272/article/details/123696963)<br>
[基于单目视觉的平面目标定位和坐标测量 (上) - 坐标系和成像模型](https://blog.csdn.net/Imkiimki/article/details/96361643)<br>
[基于单目视觉的平面目标定位和坐标测量 (下) - 相机姿态估计和目标测量](https://blog.csdn.net/Imkiimki/article/details/96748686)<br>
[摄影测量(计算机视觉)中的三角化方法](https://blog.csdn.net/Yong_Qi2015/article/details/109664717)<br>
[关于 Aruco 标记的理解并对其进行姿态估计的可视化显示](https://blog.csdn.net/qq_45445740/article/details/122296313)<br>
[一文掌握图像超分辨率重建（算法原理、Pytorch 实现）——含完整代码和数据](https://blog.csdn.net/qianbin3200896/article/details/104181552)<br>
[什么是归一化的平面坐标](https://blog.csdn.net/ouyangandy/article/details/96840781)<br>
[立体相机校准脚本](https://github.com/TemugeB/python_stereo_camera_calibrate)<br>
[多帧三角化原理](https://zhuanlan.zhihu.com/p/112307480)<br>
[相机位姿估计 3：根据两幅图像的位姿估计结果求某点的世界坐标](https://blog.csdn.net/ikke2682/article/details/54743483)<br>
[2D 坐标系与 3D 坐标系的相互转换--python 实现](http://chr10003566.github.io/2019/07/15/2D%E5%9D%90%E6%A0%87%E7%B3%BB%E4%B8%8E3D%E5%9D%90%E6%A0%87%E7%B3%BB%E7%9A%84%E7%9B%B8%E4%BA%92%E8%BD%AC%E6%8D%A2--python%E5%AE%9E%E7%8E%B0/)<br>

[根据相机位姿求指定点的世界坐标及其 python 实现](https://www.jianshu.com/p/77f7c0cd9ec7)<br>
[像素坐标转世界坐标的计算](https://www.jianshu.com/p/4566a1281066)<br>

[根据两幅图像的位姿估计结果求某点的世界坐标](https://www.cnblogs.com/singlex/p/pose_estimation_3.html)<br>
[子坐标系 C 在父坐标系 W 中的旋转问题](https://www.cnblogs.com/singlex/p/6037020.html)<br>
[机器视觉——相机标定（四个坐标系的关系）](https://blog.csdn.net/zxf1314ll/article/details/115654320)<br>
[python 下使用 aruco 标记进进行三维姿势估计](https://blog.csdn.net/dgut_guangdian/article/details/107814300)<br>
[OpenCV 基础（19）使用 OpenCV 和 Python 检测 ArUco 标记](https://blog.csdn.net/weixin_43229348/article/details/120565635)<br>
[python+opencv2 相机位姿估计](https://www.cnblogs.com/subic/p/8296794.html)<br>

[相机位姿估计 0：基本原理之如何解 PNP 问题](https://www.cnblogs.com/singlex/p/pose_estimation_0.html)<br>
[相机位姿估计 1：根据四个特征点估计相机姿态](https://www.cnblogs.com/singlex/p/pose_estimation_1.html)<br>
[相机位姿估计 1_1：OpenCV:solvePnP 二次封装与性能测试](https://www.cnblogs.com/singlex/p/pose_estimation_1_1.html)<br>
[相机位姿估计 2：[应用]实时位姿估计与三维重建相机姿态](https://www.cnblogs.com/singlex/p/pose_estimation_2.html)<br>
[相机位姿估计 3：根据两幅图像的位姿估计结果求某点的世界坐标](https://www.cnblogs.com/singlex/p/pose_estimation_3.html)<br>

[使用相机校准和 PnP 将像素坐标系 2D 坐标点 （u， v） 转换为世界坐标系 3D 坐标点 （X、Y、Z）](https://github.com/cong/2Dto3D)<br>
[2021-03-08 Python OpenCV calibrateCamera()函数](https://www.jianshu.com/p/d9c4fb366fe2)<br>
[相机内部参数矩阵获取(python+opencv)](https://zhuanlan.zhihu.com/p/420927518)<br>
[相机参数标定（camera calibration）及标定结果如何使用](https://blog.csdn.net/Aoulun/article/details/78768570)<br>
[一文带你搞懂相机内参外参(Intrinsics & Extrinsics)](https://zhuanlan.zhihu.com/p/389653208)<br>
[三维测量](https://baike.baidu.com/item/%E4%B8%89%E7%BB%B4%E6%B5%8B%E9%87%8F/10037655)<br>
[三角测量计算点的三维坐标](https://blog.csdn.net/zhaitianyong/article/details/111168657)<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>

## 相关实现

[大坝边坡无人机变形检测](https://www.sohu.com/a/463150281_120980958)<br>
[使用无人机监测建筑物的动态变形](https://www.hindawi.com/journals/mpe/2021/2657689/)<br>
[无人机变形监测解决方案（珈鹰原创）](https://www.sohu.com/a/475839582_121153551)<br>
[山体滑坡、泥石流背后的保命符！我国首个 AI 滑坡预警系统揭秘](https://zhuanlan.zhihu.com/p/354151382)<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
