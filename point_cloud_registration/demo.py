import numpy as np
from scipy.spatial.transform import Rotation as R

from solver.relaxation import linearRelaxation, semidefiniteRelaxation, StiefelRelaxation
from solver.manifold import RiemannianGradientDescent, LieGradient

from utils.data import createBunnyDataset
from utils.error import computeError
from utils.utils import se3_info

verbose = True

rng = 134
# rng = np.random.randint(2000)
data_points = 500
noise_std = 0.01
outlier_rate = 0.1
outlier_scale = 5


translation = np.random.RandomState(rng).rand(3)/np.sqrt(3)
rotation = R.random(random_state=rng).as_matrix()
data = createBunnyDataset(data_points, translation, rotation, noise_std, outlier_rate, outlier_scale, verbose=True, random_state=rng)


print("\nSolved by linear relaxation:")
model = linearRelaxation(verbose=verbose)
se3 = model.solve(data.pcd1point.copy(), data.pcd2point.copy())
sol = se3_info(se3)
computeError(estimated_rotation=sol.rotation, estimated_translation=sol.translation, 
             gtruth_rotation=data.rotation, gtruth_translation=data.translation,
             verbose=verbose)


print("\nSolved by semidefinite relaxation:")
model = semidefiniteRelaxation(verbose=verbose)
se3 = model.solve(data.pcd1point.copy(), data.pcd2point.copy())
sol = se3_info(se3)
computeError(estimated_rotation=sol.rotation, estimated_translation=sol.translation, 
             gtruth_rotation=data.rotation, gtruth_translation=data.translation,
             verbose=verbose)


print("\nSolved by Riemannian gradient descent:")
model = RiemannianGradientDescent(verbose=verbose)
se3 = model.solve(data.pcd1point.copy(), data.pcd2point.copy())
sol = se3_info(se3)
computeError(estimated_rotation=sol.rotation, estimated_translation=sol.translation, 
             gtruth_rotation=data.rotation, gtruth_translation=data.translation,
             verbose=verbose)


print("\nSolved by Lie gradient descent:")
model = LieGradient(verbose=verbose)
se3 = model.solve(data.pcd1point.copy(), data.pcd2point.copy())
sol = se3_info(se3)
computeError(estimated_rotation=sol.rotation, estimated_translation=sol.translation, 
             gtruth_rotation=data.rotation, gtruth_translation=data.translation,
             verbose=verbose)


# print("\nSolved by Stiefel relaxation:")
# model = StiefelRelaxation(verbose=verbose)
# se3 = model.solve(data.pcd1point.copy(), data.pcd2point.copy())
# sol = se3_info(se3)
# computeError(estimated_rotation=sol.rotation, estimated_translation=sol.translation, 
#              gtruth_rotation=data.rotation, gtruth_translation=data.translation,
#              verbose=verbose)

