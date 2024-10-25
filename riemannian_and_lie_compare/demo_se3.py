import numpy as np
from scipy.spatial.transform import Rotation as R

from utils.data import createToyData
from utils.se3 import mat_to_vec, vec_to_mat, hat, projection
from utils.so3 import hat as so3_hat
from utils.utils import compute_M_se3

num_points = 100
if num_points == 1:
    pcd = np.random.rand(3)
else:
    pcd = np.random.rand(num_points, 3)

rot = R.random(random_state=1).as_matrix()
t = np.random.RandomState(1).rand(3)

data = createToyData(pcd=pcd, rot=rot, t=t)
pcd1 = data.pcd1point.copy()
pcd2 = data.pcd2point.copy()

# initial guess
init_X = np.eye(4) # comment the following 2 lines for notation simplicity
init_X[:3, :3] = R.random(random_state=2).as_matrix()
init_X[:3, 3] = np.random.RandomState(2).rand(3)
x = mat_to_vec(init_X)


# Riemannian approach
mat_m = compute_M_se3(pcd1, pcd2)
gradEuclidean = 2*mat_m@x
gradEuclidean = vec_to_mat(gradEuclidean)
gradByRiemannian = projection(gradEuclidean, init_X)
print("\ngradient defined by Riemannian manifold structure:\n", gradByRiemannian)


# Lie theory approach
init_rot = init_X[:3, :3]
init_t = init_X[:3, 3]

if num_points == 1:
    Jg = np.zeros((3, 6))
    Jg[:3, :3] = -init_rot
    Jg[:3, 3:] = init_rot@so3_hat(pcd1)
    lievec = 2*Jg.T@(pcd2 - init_rot@pcd1 - init_t)
else:
    lievec = np.zeros((num_points, 6))
    for i in range(num_points):
        Jg = np.zeros((3, 6))
        Jg[:3, :3] = -init_rot
        Jg[:3, 3:] = init_rot@so3_hat(pcd1[i])
        lievec[i, :] = 2*Jg.T@(pcd2[i] - init_rot@pcd1[i] -init_t)
    lievec = np.sum(lievec, axis=0)
gradLie = hat(lievec)
gradByLie = init_X@gradLie
print("\ngradient defined by Lie theory:\n", gradByLie)