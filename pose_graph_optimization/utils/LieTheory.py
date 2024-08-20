# Implementation of 
# [1] Sola, J., Deray, J., & Atchuthan, D. (2018). 
#     A micro Lie theory for state estimation in robotics. 
#     arXiv preprint arXiv:1812.01537.
import numpy as np

def se2_vee(mat):
    ''' SE(2) to (x, y, theta) '''
    x = mat[0, 2]
    y = mat[1, 2]
    theta = np.arctan2(mat[1, 0], mat[0, 0]) # arctan(sin, cos)
    vec = np.array([x, y, theta])
    return vec

def se2_hat(vec):
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




