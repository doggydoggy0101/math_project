import numpy as np

def compute_M_so3(pcd1, pcd2):
    mat_n = np.zeros((3, 10)) 
    mat_m = np.zeros((10, 10))

    if len(pcd1.shape) == 1:
        mat_n[:, :9] = np.kron(pcd1.T, np.eye(3))
        mat_n[:, 9] = -pcd2
        mat_m += mat_n.T@mat_n
    else:
        for i in range(pcd1.shape[0]):
            mat_n[:, :9] = np.kron(pcd1[i].T, np.eye(3))
            mat_n[:, 9] = -pcd2[i]
            mat_m += mat_n.T@mat_n

    return mat_m

def compute_M_se3(pcd1, pcd2):
    mat_n = np.zeros((3, 13)) 
    mat_m = np.zeros((13, 13))

    if len(pcd1.shape) == 1:
        mat_n[:, :9] = np.kron(pcd1.T, np.eye(3))
        mat_n[:, 9:12] = np.eye(3)
        mat_n[:, 12] = -pcd2
        mat_m += mat_n.T@mat_n
    else:
        for i in range(pcd1.shape[0]):
            mat_n[:, :9] = np.kron(pcd1[i].T, np.eye(3))
            mat_n[:, 9:12] = np.eye(3)
            mat_n[:, 12] = -pcd2[i]
            mat_m += mat_n.T@mat_n

    return mat_m