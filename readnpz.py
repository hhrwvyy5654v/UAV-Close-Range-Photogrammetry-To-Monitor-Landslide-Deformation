import numpy as np

npz_path="./calibration/result/C.npz"

data=np.load(npz_path,allow_pickle=True)
for item in data.files:
    print(data[item] )