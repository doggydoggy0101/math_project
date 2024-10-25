import numpy as np

def se3_from_rot_and_t(rot, t):

    mat = np.eye(4)
    mat[:3, :3] = rot
    mat[:3, 3] = t

    return mat