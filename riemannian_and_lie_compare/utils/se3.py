import numpy as np
from utils.so3 import hat as so3_hat
from utils.so3 import projection as so3_projection

def mat_to_vec(mat):
    return np.array([mat[0, 0], mat[1, 0], mat[2, 0], 
                     mat[0, 1], mat[1, 1], mat[2, 1], 
                     mat[0, 2], mat[1, 2], mat[2, 2],
                     mat[0, 3], mat[1, 3], mat[2, 3],
                     1.0])

def vec_to_mat(vec):
    return np.array([[vec[0], vec[3], vec[6], vec[9]],
                     [vec[1], vec[4], vec[7], vec[10]],
                     [vec[2], vec[5], vec[8], vec[11]],
                     [0.0, 0.0, 0.0, 1.0]])

def hat(lie):
    rho = lie[:3]
    rot_vec = lie[3:]
    mat = np.zeros((4, 4))

    mat[:3, :3] = so3_hat(rot_vec)
    mat[:3, 3] = rho
    return mat

def projection(mat, se3):
    proj = np.zeros((4, 4))
    proj[:3, :3] = so3_projection(mat[:3, :3], se3[:3, :3])
    proj[:3, 3] = mat[:3, 3]
    return proj