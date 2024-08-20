import numpy as np
# from scipy.spatial.transform import Rotation as R

def get_zero_mean_point_cloud(pcd):

    mean = np.mean(pcd, axis=0)
    pcd -= mean

    return pcd, mean

def project(mat):
    """ orthogonal Procrustes problem """
    assert mat.shape[0] == mat.shape[1], "Matrix must be square"
    assert mat.shape[0] == 3, "Matrix must be 3x3"

    U, _, Vt = np.linalg.svd(mat)
    rot = U@Vt

    # reflection case
    if np.linalg.det(rot) < 0:
        D = np.diag(np.array([1.0, 1.0, -1.0]))
        rot = U@D@Vt
    
    return rot
    
def compute_initial_guess(pcd1, pcd2):
    
    pcd1, mean1 = get_zero_mean_point_cloud(pcd1)
    pcd2, mean2 = get_zero_mean_point_cloud(pcd2)

    mat = np.eye(4)
    mat[:3, :3] = project(pcd2.T@pcd1)
    mat[:3, 3] = mean2 - mean1

    return mat

def compute_mat(pcd1, pcd2):

    id3 = np.eye(3)
    mat = np.zeros((13, 13))
    for i in range(pcd1.shape[0]):
        mat_n = np.zeros((3, 13))
        mat_n[:, :9] = np.kron(pcd1[i].T, id3)
        mat_n[:, 9:12] = id3
        mat_n[:, 12] = -pcd2[i]

        mat_m = mat_n.T@mat_n
        mat += mat_m
    return mat


def se3_mat_to_vec(mat):
    return np.array([mat[0, 0], mat[1, 0], mat[2, 0], 
                     mat[0, 1], mat[1, 1], mat[2, 1], 
                     mat[0, 2], mat[1, 2], mat[2, 2],
                     mat[0, 3], mat[1, 3], mat[2, 3],
                     1.0])

def se3_vec_to_mat(vec):
    return np.array([[vec[0], vec[3], vec[6], vec[9]],
                     [vec[1], vec[4], vec[7], vec[10]],
                     [vec[2], vec[5], vec[8], vec[11]],
                     [0.0, 0.0, 0.0, 1.0]])

def se3_vec_to_r_and_t(vec):
    rot = np.array([[vec[0], vec[3], vec[6]],
                    [vec[1], vec[4], vec[7]],
                    [vec[2], vec[5], vec[8]]])
    t = np.array([vec[9], vec[10], vec[11]])
    return rot, t

def se3_projection(vec, x):
    ''' project an Euclidean space mat to the tangent space of se3 '''
    w_x = x[6]*vec[3] + x[7]*vec[4] + x[8]*vec[5] - x[3]*vec[6] - x[4]*vec[7] - x[5]*vec[8]
    w_y = x[0]*vec[6] + x[1]*vec[7] + x[2]*vec[8] - x[6]*vec[0] - x[7]*vec[1] - x[8]*vec[2]
    w_z = x[3]*vec[0] + x[4]*vec[1] + x[5]*vec[2] - x[0]*vec[3] - x[1]*vec[4] - x[2]*vec[5]
    
    return np.array([x[3]*w_z - x[6]*w_y, x[4]*w_z - x[7]*w_y, x[5]*w_z - x[8]*w_y, 
                     x[6]*w_x - x[0]*w_z, x[7]*w_x - x[1]*w_z, x[8]*w_x - x[2]*w_z, 
                     x[0]*w_y - x[3]*w_x, x[1]*w_y - x[4]*w_x, x[2]*w_y - x[5]*w_x,
                     vec[9], vec[10], vec[11], 0.0])

def se3_retraction(vec, x):

    rot = project(np.array([[x[0] + vec[0], x[3] + vec[3], x[6] + vec[6]],
                            [x[1] + vec[1], x[4] + vec[4], x[7] + vec[7]],
                            [x[2] + vec[2], x[5] + vec[5], x[8] + vec[8]]]))
    
    return np.array([rot[0, 0], rot[1, 0], rot[2, 0],
                     rot[0, 1], rot[1, 1], rot[2, 1],
                     rot[0, 2], rot[1, 2], rot[2, 2],
                     x[9] + vec[9], x[10] + vec[10], x[11] + vec[11], 1])

def se3_norm(vec):
    return np.linalg.norm(np.array([[vec[0], vec[3], vec[6]],
                                    [vec[1], vec[4], vec[7]],
                                    [vec[2], vec[5], vec[8]]])) + np.linalg.norm(vec[9:12])

def so3_hat(lie):
    return np.array([[0, -lie[2], lie[1]],
                     [lie[2], 0, -lie[0]],
                     [-lie[1], lie[0], 0]])

def se3_hat(lie):
    rho = lie[:3]
    rot_vec = lie[3:]
    mat = np.zeros((4, 4))

    mat[:3, :3] = so3_hat(rot_vec)
    mat[:3, 3] = rho
    return mat


def se3_Exp(lie):
    
    rho = lie[:3]
    rot_vec = lie[3:]
    mat = np.eye(4)

    theta = np.linalg.norm(rot_vec)
    mu = rot_vec/theta
    skew = so3_hat(mu)
    mat[:3, :3] = np.eye(3) + np.sin(theta)*skew + (1 - np.cos(theta))*skew@skew # so3 Exp map

    mat_v = np.eye(3) + ((1 - np.cos(theta))/theta)*skew + ((theta - np.sin(theta))/theta)*skew@skew
    mat[:3, 3] = mat_v@rho

    return mat

class se3_info:
    def __init__(self, se3):
        self.se3 = se3
        self.rotation = se3[:3, :3]
        self.translation = se3[:3, 3]



def so3_constraints(idx):
    ''' SDP constraints of SO(3) in registration problems (from 1 to 22) '''

    mat_a = np.zeros((13, 13))

    if idx == 1:
        for i in range(3): mat_a[i][i] = 1
        mat_a[-1, -1] = -1

    if idx == 2:
        for i in range(3): mat_a[i+3][i+3] = 1
        mat_a[-1, -1] = -1

    if idx == 3:
        for i in range(3): mat_a[i+6][i+6] = 1
        mat_a[-1, -1] = -1

    if idx == 4:
        for i in range(3): mat_a[i, i+3] = 1/2
        mat_a += mat_a.T

    if idx == 5:
        for i in range(3): mat_a[i, i+6] = 1/2
        mat_a += mat_a.T

    if idx == 6:
        for i in range(3): mat_a[i+3, i+6] = 1/2
        mat_a += mat_a.T

    if idx == 7:
        for i in range(3): mat_a[3*i, 3*i] = 1
        mat_a[-1, -1] = -1

    if idx == 8:
        for i in range(3): mat_a[3*i+1, 3*i+1] = 1
        mat_a[-1, -1] = -1

    if idx == 9:
        for i in range(3): mat_a[3*i+2, 3*i+2] = 1
        mat_a[-1, -1] = -1

    if idx == 10:
        for i in range(3): mat_a[3*i, 3*i+1] = 1/2
        mat_a += mat_a.T

    if idx == 11:
        for i in range(3): mat_a[3*i, 3*i+2] = 1/2
        mat_a += mat_a.T

    if idx == 12:
        for i in range(3): mat_a[3*i+1, 3*i+2] = 1/2
        mat_a += mat_a.T

    if idx == 13:
        mat_a[4, 8], mat_a[5, 7], mat_a[0, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T

    if idx == 14:
        mat_a[5, 6], mat_a[3, 8], mat_a[1, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T

    if idx == 15:
        mat_a[3, 7], mat_a[4, 6], mat_a[2, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T

    if idx == 16:
        mat_a[2, 7], mat_a[1, 8], mat_a[3, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T

    if idx == 17:
        mat_a[0, 8], mat_a[2, 6], mat_a[4, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T

    if idx == 18:
        mat_a[1, 6], mat_a[0, 7], mat_a[5, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T

    if idx == 19:
        mat_a[1, 5], mat_a[2, 4], mat_a[6, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T

    if idx == 20:
        mat_a[2, 3], mat_a[0, 5], mat_a[7, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T
    
    if idx == 21:
        mat_a[0, 4], mat_a[1, 3], mat_a[8, -1] = 1/2 , -1/2, -1/2
        mat_a += mat_a.T
    
    if idx == 22:
        mat_a [-1, -1] = 1

    return mat_a