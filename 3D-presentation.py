'''
Description: 使用3D箭头图展示多个监测点世界坐标系的变化
FilePath: \3D-presentation.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-05-08 11:37:50
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-14 11:06:43
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 监测到的多个点的坐标变化数据
# 每个数组包含相应坐标分量的前后值
points = [
    {'before': [150, -50, 0], 'after': [173.2259, -57.746193, 5.4546866]},
    {'before': [150, 50, 0], 'after': [168.65923, 41.87658, 5.7979345]},
]

# 创建3D箭头图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 颜色列表
colors = ['red', 'blue', 'green', 'yellow', 'black', 'white',
          'gray', 'cyan', 'magenta', 'orange', 'pink', 'purple', 'brown']

# 绘制箭头
for i, point in enumerate(points):
    x_before, y_before, z_before = point['before']
    x_after, y_after, z_after = point['after']
    dx = x_after - x_before
    dy = y_after - y_before
    dz = z_after - z_before
    ax.quiver(x_before, y_before, z_before, dx, dy,
              dz, color=colors[i % len(colors)], arrow_length_ratio=0.1)
    print(colors[i % len(colors)],
          "{", point['before'], "--->", point['after'], "}")

# 设置坐标轴标签
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# 设置标题
ax.set_title('监测点的世界坐标(X,Y,Z)变化的3D箭头图')

# 设置坐标轴范围
all_x = [point['before'][0]
         for point in points] + [point['after'][0] for point in points]
all_y = [point['before'][1]
         for point in points] + [point['after'][1] for point in points]
all_z = [point['before'][2]
         for point in points] + [point['after'][2] for point in points]

ax.set_xlim(min(all_x), max(all_x))
ax.set_ylim(min(all_y), max(all_y))
ax.set_zlim(min(all_z), max(all_z))

# 显示图形
plt.show()
