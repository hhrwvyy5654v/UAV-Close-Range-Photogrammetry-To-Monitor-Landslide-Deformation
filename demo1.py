import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 假设这是您监测到的点的坐标变化数据
# 每个数组包含相应坐标分量的前后值
x = [1, 1.2]
y = [2, 2.1]
z = [3, 2.8]

# 计算箭头的方向和长度
dx = x[1] - x[0]
dy = y[1] - y[0]
dz = z[1] - z[0]

# 创建3D箭头图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制箭头
ax.quiver(x[0], y[0], z[0], dx, dy, dz, color='b', arrow_length_ratio=0.1)

# 设置坐标轴标签
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# 设置标题
ax.set_title('3D Arrow Plot of World Coordinates (X, Y, Z) Change')

# 设置坐标轴范围
ax.set_xlim(min(x), max(x))
ax.set_ylim(min(y), max(y))
ax.set_zlim(min(z), max(z))

# 显示图形
plt.show()
