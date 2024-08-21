# Implementation of 
# [1] Sola, J., Deray, J., & Atchuthan, D. (2018). 
#     A micro Lie theory for state estimation in robotics. 
#     arXiv preprint arXiv:1812.01537.
import numpy as np

def se2_mat_to_vec(mat):
    ''' SE(2) to (x, y, theta) '''
    x = mat[0, 2]
    y = mat[1, 2]
    theta = np.arctan2(mat[1, 0], mat[0, 0]) # arctan(sin, cos)
    vec = np.array([x, y, theta])
    return vec

def se2_vec_to_mat(vec):
    ''' (x, y, theta) to SE(2) '''
    theta = vec[2]
    mat = np.array([[np.cos(theta), -np.sin(theta), vec[0]], [np.sin(theta), np.cos(theta), vec[1]], [0.0, 0.0, 1.0]])
    return mat

def so2_hat(lie):
    ''' Equation (113) of [1] '''
    return np.array([[0.0, -lie], [lie, 0.0]])

def se2_Log(mat):
    rot  = mat[:2, :2]
    theta = np.arctan2(rot[1, 0], rot[0, 0]) # arctan(sin, cos)
    t = mat[:2, 2]

    mat_v = (np.sin(theta)/theta)*np.eye(2) + ((1 - np.cos(theta))/theta)*so2_hat(1.0)

    lie = np.zeros(3)
    lie[:2] = np.linalg.inv(mat_v)@t
    lie[2] = theta

    return lie

def se2_Jacobian_right(lie):
    x = lie[0]
    y = lie[1]
    theta = lie[2]

    J_r = np.eye(3)
    J_r[0, 0] = np.sin(theta)/theta
    J_r[0, 1] = (1 - np.cos(theta))/theta
    J_r[1, 0] = (np.cos(theta) - 1)/theta
    J_r[1, 1] = np.sin(theta)/theta
    J_r[0, 2] = (theta*x - y -np.sin(theta)*x + np.cos(theta)*y)/(theta**2)
    J_r[1, 2] = (x + theta*y -np.cos(theta)*x - np.sin(theta)*y)/(theta**2)

    return J_r

def se2_Jacobian_inversion(se2):
    rot  = se2[:2, :2]
    t = se2[:2, 2]

    J_inv = -np.eye(3)
    J_inv[:2, :2] = -rot
    J_inv[:2, 2] = so2_hat(1)@t

    return J_inv