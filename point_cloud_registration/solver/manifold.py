import numpy as np

import time

from utils.utils import compute_initial_guess, compute_mat
from utils.utils import se3_mat_to_vec, se3_vec_to_mat, se3_vec_to_r_and_t
from utils.utils import se3_projection, se3_retraction, se3_norm
from utils.utils import so3_hat, se3_hat, se3_Exp
from utils.line_search import BackTrackingLineSearch

class RiemannianGradientDescent:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def solve(self, pcd1, pcd2, max_iter=1000, min_grad_norm=1e-6, min_step_size=1e-10):
        assert pcd1.shape == pcd2.shape, "Input point clouds must have the same shape"
        if self.verbose:
            tic = time.time()

        # init_mat = compute_initial_guess(pcd1.copy(), pcd2.copy())
        init_mat = np.eye(4)
        x = se3_mat_to_vec(init_mat)

        mat_m = compute_mat(pcd1, pcd2)

        def objective(x):
            return x.T@mat_m@x

        line_search = BackTrackingLineSearch()

        for i in range(max_iter):

            gradEuclidean = 2*mat_m@x
            gradRiemannian = se3_projection(gradEuclidean, x) # projection to the tangent space of se3_x
            grad_norm = se3_norm(gradRiemannian)

            x, step_size = line_search.search(objective, se3_retraction, se3_norm, x, -gradRiemannian, objective(x), -(grad_norm**2))
   
            if grad_norm < min_grad_norm or step_size < min_step_size:
                if self.verbose:
                    print("-- rgd: {} iterations".format(i+1))
                break

        se3 = se3_vec_to_mat(x)

        if self.verbose:
            toc = time.time()
            print("estimated rotation:\n", se3[:3, :3])
            print("estimated translation:", se3[:3, 3])
            print("time elapsed: {:.5f} sec".format(toc - tic))
        return se3
        


class LieGradient:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def skew(self, vec):
        return np.array([[0, -vec[2], vec[1]],
                         [vec[2], 0, -vec[0]],
                         [-vec[1], vec[0], 0]])

    def computeLieJacobian(self, x):

        rot, t = se3_vec_to_r_and_t(x)
        J = np.zeros((self.num, 6))

        for j in range(self.num):
            Jg = np.zeros((3, 6))
            Jg[:3, :3] = -rot
            Jg[:3, 3:] = rot@so3_hat(self.pcd1[j])
            J[j, :] = 2*Jg.T@(self.pcd2[j] - rot@self.pcd1[j] - t)
        return np.sum(J, axis=0)

    def gradient_descent(self, x, mat_m, max_iter=1000, min_grad_norm=1e-6, min_step_size=1e-10):

        def objective(x):
            return x.T@mat_m@x

        line_search = BackTrackingLineSearch()

        for i in range(max_iter):

            gradLie = self.computeLieJacobian(x)
            gradRiemannian = se3_mat_to_vec(se3_vec_to_mat(x)@se3_hat(gradLie))
            grad_norm = se3_norm(gradRiemannian)

            x, step_size = line_search.search(objective, se3_retraction, se3_norm, x, -gradRiemannian, objective(x), -(grad_norm**2))
   
            if grad_norm < min_grad_norm or step_size < min_step_size:
                if self.verbose:
                    print("-- rgd: {} iterations".format(i+1))
                break
        return x

    def solve(self, pcd1, pcd2):
        assert pcd1.shape == pcd2.shape, "Input point clouds must have the same shape"
        if self.verbose:
            tic = time.time()

        self.pcd1 = pcd1
        self.pcd2 = pcd2
        self.num = self.pcd1.shape[0]

        # init_mat = compute_initial_guess(pcd1.copy(), pcd2.copy())
        init_mat = np.eye(4)
        x = se3_mat_to_vec(init_mat)

        mat_m = compute_mat(pcd1, pcd2)
        x = self.gradient_descent(x, mat_m)
        se3 = se3_vec_to_mat(x)

        if self.verbose:
            toc = time.time()
            print("estimated rotation:\n", se3[:3, :3])
            print("estimated translation:", se3[:3, 3])
            print("time elapsed: {:.5f} sec".format(toc - tic))
        return se3