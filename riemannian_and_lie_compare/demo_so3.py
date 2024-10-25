import numpy as np
from scipy.spatial.transform import Rotation as R

from utils.data import createToyData
from utils.so3 import mat_to_vec, vec_to_mat, hat, projection
from utils.utils import compute_M_so3

num_points = 1
if num_points == 1:
    pcd = np.array([1.0, 2.0, 3.0])
    # pcd = np.random.rand(3)
else:
    pcd = np.random.rand(num_points, 3)

rot = R.random(random_state=1).as_matrix()

data = createToyData(pcd=pcd, rot=rot)
pcd1 = data.pcd1point.copy()
pcd2 = data.pcd2point.copy()


# initial guess
init_X = np.eye(3) # for notation simplicity
# init_X = R.random(random_state=2).as_matrix()
x = mat_to_vec(init_X)


# Riemannian approach
mat_m = compute_M_so3(pcd1, pcd2)
gradEuclidean = 2*mat_m@x
gradEuclidean = vec_to_mat(gradEuclidean)
gradByRiemannian = projection(gradEuclidean, init_X)
print("\ngradient defined by Riemannian manifold structure:\n", gradByRiemannian)


# Lie theory approach
if num_points == 1:
    lievec = 2*hat(pcd1).T@init_X.T@(pcd2 - init_X@pcd1)
else:
    lievec = np.zeros((num_points, 3))
    for i in range(num_points):
        lievec[i, :] = 2*hat(pcd1[i]).T@init_X.T@(pcd2[i] - init_X@pcd1[i])
    lievec = np.sum(lievec, axis=0)
gradLie = hat(lievec)
gradByLie = init_X@gradLie
print("\ngradient defined by Lie theory:\n", gradByLie)