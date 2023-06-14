import csv
import numpy as np

csv_name='./ArucoShot/PixelCoordinates.csv'


def Get_the_pixel_coordinates(csv_name,image_name):
    Pixel_coordinates = []
    with open(csv_name, 'r') as file:
        reader = csv.reader(file)
        next(reader) # 跳过第一行标题行
        for row in reader:
            if not row: # 检查该行是否为空
                continue
            if row[0]==image_name:
                aruco_id = int(row[1])
                x = float(row[2])
                y = float(row[3])
                Pixel_coordinates.append((aruco_id, [x, y]))
        Pixel_coordinates.sort(key=lambda x: x[0])
        Pixel_coordinates = [x[1] for x in Pixel_coordinates]
        return np.array(Pixel_coordinates[:-2], dtype=np.float32)

image_name="IMG_20230531_105515.jpg"

print(Get_the_pixel_coordinates(csv_name,image_name))