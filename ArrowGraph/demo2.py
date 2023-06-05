import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 监测到的多个点的坐标变化数据
# 每个数组包含相应坐标分量的前后值
points = [
    {'before': [-50, -50, 0], 'after': [-70, 60, 13]},
    {'before': [-50, 50, 0], 'after': [-40, 30, 20]},
    {'before': [50, -50, 0], 'after': [60, -80, 90]},
    {'before': [50, 50, 0], 'after': [20, 50, 33]},
]


# 创建3D箭头图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制箭头
for point in points:
    x_before, y_before, z_before = point['before']
    x_after, y_after, z_after = point['after']
    dx = x_after - x_before
    dy = y_after - y_before
    dz = z_after - z_before
    ax.quiver(x_before, y_before, z_before, dx, dy,
              dz, color='b', arrow_length_ratio=0.1)

# 设置坐标轴标签
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# 设置标题
ax.set_title('多点世界坐标(X,Y,Z)变化的3D箭头图')

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
