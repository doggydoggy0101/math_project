import numpy as np

def mat_to_vec(mat):
    return np.array([mat[0, 0], mat[1, 0], mat[2, 0],
                     mat[0, 1], mat[1, 1], mat[2, 1],
                     mat[0, 2], mat[1, 2], mat[2, 2], 1.0])

def vec_to_mat(vec):
    return np.array([[vec[0], vec[3], vec[6]],
                     [vec[1], vec[4], vec[7]],
                     [vec[2], vec[5], vec[8]]])

def hat(vec):
    return np.array([[0, -vec[2], vec[1]],
                     [vec[2], 0, -vec[0]],
                     [-vec[1], vec[0], 0]])

def projection(mat, so3):
    return so3@(so3.T@mat - mat.T@so3) # omit division by 2 to match Lie theory