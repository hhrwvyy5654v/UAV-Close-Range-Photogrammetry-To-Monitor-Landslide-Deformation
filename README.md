<!--
 * @Editor: Microsoft VS Code
 * @Author: HuangRongQuan
 * @version: 
 * @Date: 2023-03-27 09:53:13
 * @LastEditors: 
 * @LastEditTime: 2023-04-21 15:31:14
 * @FilePath: \UAV-close-range-photogrammetry-to-monitor-landslide-deformation-main\README.md
 * @Descripttion: 
-->

# **<center>无人机近景摄影测量监测滑坡形变</center>**

![](Assets/无人机近景摄影测量监测滑坡形变.png)<br>

![](Assets/视频位移监测使用示意.jpg)<br>


## 参考文章
[计算机视觉对极几何之Triangulate(三角化)](https://blog.csdn.net/u011178262/article/details/86729887)<br>
[关于Aruco标记的理解并对其进行姿态估计的可视化显示](https://blog.csdn.net/qq_45445740/article/details/122296313)<br>
[三角形法恢复空间点深度](https://blog.csdn.net/kokerf/article/details/72844455)<br>
[三角化特征点(triangulation)方法及实现对比](https://blog.csdn.net/weixin_41469272/article/details/123696963)<br>
[基于单目视觉的平面目标定位和坐标测量 (上) - 坐标系和成像模型](https://blog.csdn.net/Imkiimki/article/details/96361643)<br>
[基于单目视觉的平面目标定位和坐标测量 (下) - 相机姿态估计和目标测量](https://blog.csdn.net/Imkiimki/article/details/96748686)<br>
[摄影测量(计算机视觉)中的三角化方法](https://blog.csdn.net/Yong_Qi2015/article/details/109664717)<br>
[关于Aruco标记的理解并对其进行姿态估计的可视化显示](https://blog.csdn.net/qq_45445740/article/details/122296313)<br>
[一文掌握图像超分辨率重建（算法原理、Pytorch实现）——含完整代码和数据](https://blog.csdn.net/qianbin3200896/article/details/104181552)<br>
[什么是归一化的平面坐标](https://blog.csdn.net/ouyangandy/article/details/96840781)<br>
[立体相机校准脚本](https://github.com/TemugeB/python_stereo_camera_calibrate)<br>
[多帧三角化原理](https://zhuanlan.zhihu.com/p/112307480)<br>
[相机位姿估计3：根据两幅图像的位姿估计结果求某点的世界坐标](https://blog.csdn.net/ikke2682/article/details/54743483)<br>
[2D坐标系与3D坐标系的相互转换--python实现](http://chr10003566.github.io/2019/07/15/2D%E5%9D%90%E6%A0%87%E7%B3%BB%E4%B8%8E3D%E5%9D%90%E6%A0%87%E7%B3%BB%E7%9A%84%E7%9B%B8%E4%BA%92%E8%BD%AC%E6%8D%A2--python%E5%AE%9E%E7%8E%B0/)<br>

[根据相机位姿求指定点的世界坐标及其python实现](https://www.jianshu.com/p/77f7c0cd9ec7)<br>
[像素坐标转世界坐标的计算](https://www.jianshu.com/p/4566a1281066)<br>

[根据两幅图像的位姿估计结果求某点的世界坐标](https://www.cnblogs.com/singlex/p/pose_estimation_3.html)<br>
[子坐标系C在父坐标系W中的旋转问题](https://www.cnblogs.com/singlex/p/6037020.html)<br>
[机器视觉——相机标定（四个坐标系的关系）](https://blog.csdn.net/zxf1314ll/article/details/115654320)<br>
[python下使用aruco标记进进行三维姿势估计](https://blog.csdn.net/dgut_guangdian/article/details/107814300)<br>
[OpenCV基础（19）使用 OpenCV 和 Python 检测 ArUco 标记](https://blog.csdn.net/weixin_43229348/article/details/120565635)<br>
[python+opencv2相机位姿估计](https://www.cnblogs.com/subic/p/8296794.html)<br>

[相机位姿估计0：基本原理之如何解PNP问题](https://www.cnblogs.com/singlex/p/pose_estimation_0.html)<br>
[相机位姿估计1：根据四个特征点估计相机姿态](https://www.cnblogs.com/singlex/p/pose_estimation_1.html)<br>
[相机位姿估计1_1：OpenCV:solvePnP二次封装与性能测试](https://www.cnblogs.com/singlex/p/pose_estimation_1_1.html)<br>
[相机位姿估计2：[应用]实时位姿估计与三维重建相机姿态](https://www.cnblogs.com/singlex/p/pose_estimation_2.html)<br>
[相机位姿估计3：根据两幅图像的位姿估计结果求某点的世界坐标](https://www.cnblogs.com/singlex/p/pose_estimation_3.html)<br>

[使用相机校准和 PnP 将像素坐标系 2D 坐标点 （u， v） 转换为世界坐标系 3D 坐标点 （X、Y、Z）](https://github.com/cong/2Dto3D)<br>
[2021-03-08 Python OpenCV calibrateCamera()函数](https://www.jianshu.com/p/d9c4fb366fe2)<br>
[相机内部参数矩阵获取(python+opencv)](https://zhuanlan.zhihu.com/p/420927518)<br>
[相机参数标定（camera calibration）及标定结果如何使用](https://blog.csdn.net/Aoulun/article/details/78768570)<br>
[一文带你搞懂相机内参外参(Intrinsics & Extrinsics)](https://zhuanlan.zhihu.com/p/389653208)<br>
[]()<br>
[]()<br>
[]()<br>



## 相关实现
[大坝边坡无人机变形检测](https://www.sohu.com/a/463150281_120980958)<br>
[使用无人机监测建筑物的动态变形](https://www.hindawi.com/journals/mpe/2021/2657689/)<br>
[无人机变形监测解决方案（珈鹰原创）](https://www.sohu.com/a/475839582_121153551)<br>
[山体滑坡、泥石流背后的保命符！我国首个AI滑坡预警系统揭秘](https://zhuanlan.zhihu.com/p/354151382)<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>
[]()<br>


