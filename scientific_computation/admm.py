import numpy as np
import cvxpy as cp
import scipy as sp
import time

np.random.seed(1)

class regressionLASSO:
    def __init__(self, num_row, num_col, gamma, verbose=True):
        self.gamma = gamma
        self.verbose = verbose

        self.m = num_row 
        self.n = num_col 

        self.A, self.gtruth = self.generateData()
        self.b = self.A@self.gtruth + 0.5*np.random.randn()
    
    def generateData(self):

        A = sp.sparse.random(self.m, self.n, density=0.5)
        x = (np.random.rand(self.n) > 0.8).astype(float)*np.random.randn(self.n)/np.sqrt(self.n)

        return A, x
        

    def linearRegression(self):
        ''' Least Sqaures '''
        x = cp.Variable(self.n)
        prob = cp.Problem(cp.Minimize((1/2)*cp.sum_squares(self.A@x - self.b)))

        tic = time.time()
        prob.solve()
        toc = time.time()
        
        estimate = x.value
        if self.verbose:
            print("\nLS")
            print("mean square error: {:.5f}".format(np.linalg.norm(self.gtruth - estimate)))
            print("computational time: {:.5f} sec".format(toc-tic))
        return estimate


    def lassoRegression(self, solver=None):
        ''' LASSO by different solvers '''
        x = cp.Variable(self.n)
        prob = cp.Problem(cp.Minimize((1/2)*cp.sum_squares(self.A@x - self.b) + self.gamma*cp.norm1(x)))

        if solver == "CVXOPT":
            tic = time.time()
            prob.solve(solver=cp.CVXOPT)
            toc = time.time()
        elif solver == "MOSEK":
            tic = time.time()
            prob.solve(solver=cp.MOSEK)
            toc = time.time()
        elif solver == "OSQP": # ADMM
            tic = time.time()
            prob.solve(solver=cp.OSQP)
            toc = time.time()

        estimate = x.value
        if self.verbose:
            print("\nLASSO", solver)
            print("mean square error: {:.5f}".format(np.linalg.norm(self.gtruth - estimate)))
            print("computational time: {:.5f} sec".format(toc-tic))
        return estimate



if __name__ == "__main__":

    num_row = 1000
    num_col = 10
    gamma = 3

    model = regressionLASSO(num_row, num_col, gamma)
    time.sleep(2)
    model.linearRegression()
    time.sleep(2)
    model.lassoRegression(solver="CVXOPT")
    time.sleep(2)
    model.lassoRegression(solver="MOSEK")
    time.sleep(2)
    model.lassoRegression(solver="OSQP")