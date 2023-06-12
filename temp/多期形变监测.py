'''
Description: 
FilePath: \无人机建筑沉降监测\多期形变监测.py
Author: hhrwvyy5654v huang_rongquan@outlook.com
Date: 2023-06-09 15:44:00
LastEditors: hhrwvyy5654v huang_rongquan@outlook.com
LastEditTime: 2023-06-09 15:44:00
Copyright (c) 2023 by hhrwvyy5654v , All Rights Reserved. 
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 假设有三期的监测点数据
data = {
    '期1': np.array([[50, 50, 50], [75, 75, 75], [100, 100, 100]]),
    '期2': np.array([[55, 55, 55], [80, 80, 80], [110, 110, 110]]),
    '期3': np.array([[45, 45, 45], [45, 45, 45], [90, 90, 90]]),
}

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['r', 'g', 'b']
markers = ['o', '^', 's']

for i, (label, points) in enumerate(data.items()):
    x, y, z = points.T
    ax.scatter(x, y, z, c=colors[i], marker=markers[i], label=label)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

plt.show()
