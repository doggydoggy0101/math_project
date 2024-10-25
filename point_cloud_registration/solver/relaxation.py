import numpy as np
import cvxpy as cp
import scipy as sp
import time

from utils.utils import compute_mat, so3_constraints, se3_vec_to_mat
from utils.utils import project, se3_vec_to_mat

class linearRelaxation:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def solve(self, pcd1, pcd2):
        assert pcd1.shape == pcd2.shape, "Input point clouds must have the same shape"
        e = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
        if self.verbose:
            tic = time.time()

        mat_m = compute_mat(pcd1, pcd2)

        lu, piv = sp.linalg.lu_factor(mat_m)
        temp = sp.linalg.lu_solve((lu, piv), e)
        x = (1/(e@temp))*temp

        se3 = se3_vec_to_mat(x)
        se3[:3, :3] = project(se3[:3, :3])

        if self.verbose:
            toc = time.time()
            print("estimated rotation:\n", se3[:3, :3])
            print("estimated translation:", se3[:3, 3])
            print("time elapsed: {:.5f} sec".format(toc - tic))
        return se3



class semidefiniteRelaxation:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def solve(self, pcd1, pcd2):
        assert pcd1.shape == pcd2.shape, "Input point clouds must have the same shape"
        if self.verbose:
            tic = time.time()

        mat_m = compute_mat(pcd1, pcd2)

        var_z = cp.Variable((13, 13), PSD=True) 
        constraints = [cp.trace(so3_constraints(22)@var_z) == 1]
        for i in range(21):
            constraints += [cp.trace(so3_constraints(i+1)@var_z) == 0]  

        prob = cp.Problem(cp.Minimize(cp.trace(mat_m@var_z)), constraints)
        prob.solve(solver=cp.MOSEK)
        mat_z = var_z.value

        U, d, _ = np.linalg.svd(mat_z) 
        
        null_index = np.where(np.round(d, 5) == 0)[0]
        rank = 13 - len(null_index) # rank-nullity theorem
        tight = True if rank == 1 else False # tightness of relaxation

        x = U[:, np.where(d == np.max(d))[0]].reshape(13) # eigenvector associated with the maximum eigenvalue
        x /= x[-1] # dehomogeneize

        se3 = se3_vec_to_mat(x)

        if self.verbose:
            toc = time.time()
            print("relaxation is tight:", tight)
            print("estimated rotation:\n", se3[:3, :3])
            print("estimated translation:", se3[:3, 3])
            print("time elapsed: {:.5f} sec".format(toc - tic))
        return se3


class StiefelRelaxation:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def construct_matrix(self, var):
        ''' construct enlarged PSD variable for cvx '''

        cp3 = cp.Parameter((3,3))
        cp3.value = np.eye(3)

        rot = cp.vstack([cp.hstack([var[0], var[3], var[6]]),
                         cp.hstack([var[1], var[4], var[7]]),
                         cp.hstack([var[2], var[5], var[8]])])

        return cp.vstack([cp.hstack([cp3, rot]), cp.hstack([rot.T, cp3])])

    def solve_x(self, x, terms):

        mat_q = np.zeros((13, 13))
        for mat_i in terms:
            mat_q += mat_i/((x@mat_i@x + self.c**2)**2)

        var_x = cp.Variable(13)
        var_z = self.construct_matrix(var_x)

        constraints = [var_x[-1] == 1]
        constraints += [var_z >> 0]

        prob = cp.Problem(cp.Minimize(cp.quad_form(var_x, mat_q)), constraints)
        prob.solve(solver=cp.MOSEK)
        return var_x.value


    def solve(self, pcd1, pcd2):
        assert pcd1.shape == pcd2.shape, "Input point clouds must have the same shape"
        if self.verbose:
            tic = time.time()

        mat_m = compute_mat(pcd1, pcd2)

        var_x = cp.Variable(13)
        var_z = self.construct_matrix(var_x)

        constraints = [var_x[-1] == 1]
        constraints += [var_z >> 0]

        prob = cp.Problem(cp.Minimize(cp.quad_form(var_x, mat_m)), constraints)
        prob.solve(solver=cp.MOSEK)

        x = var_x.value
        se3 = se3_vec_to_mat(x)
        se3[:3, :3] = project(se3[:3, :3])
        
        if self.verbose:
            toc = time.time()
            print("estimated rotation:\n", se3[:3, :3])
            print("estimated translation:", se3[:3, 3])
            print("time elapsed: {:.5f} sec".format(toc - tic))
        return se3



