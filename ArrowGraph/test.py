
import numpy as np
import trimesh
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mesh = trimesh.load('model.stl')
vertices = mesh.vertices
faces = mesh.faces

dx, dy, dz = [1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15]
new_vertices = np.zeros_like(vertices)
for i in range(vertices.shape[0]):
    new_vertices[i][0] = vertices[i][0] + dx[i]
    new_vertices[i][1] = vertices[i][1] + dy[i]
    new_vertices[i][2] = vertices[i][2] + dz[i]

deformation = [0.1, 0.2, 0.3, 0.4, 0.5]
colors = np.zeros((vertices.shape[0], 3))
for i in range(faces.shape[0]):
    c = deformation[i]
    for j in range(3):
        colors[faces[i][j]] += c
colors /= colors.max()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(new_vertices[:, 0], new_vertices[:, 1], new_vertices[:, 2], triangles=faces, cmap='viridis', linewidth=0.2, antialiased=True, shade=True, facecolors=colors)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 假设有两个时间点的滑坡监测数据
data1 = np.array([[1, 10, 20, 30],
                  [2, 15, 25, 35],
                  [3, 20, 30, 40]])

data2 = np.array([[1, 11, 21, 31],
                  [2, 16, 26, 36],
                  [3, 21, 31, 41]])

# 创建3D绘图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制第一个时间点的数据（用红色表示）
ax.scatter(data1[:, 1], data1[:, 2], data1[:, 3], c='r', marker='o', label='Time 1')

# 绘制第二个时间点的数据（用蓝色表示）
ax.scatter(data2[:, 1], data2[:, 2], data2[:, 3], c='b', marker='^', label='Time 2')

# 添加坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 添加图例
ax.legend()

# 显示图形
plt.show()
