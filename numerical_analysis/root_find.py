import numpy as np

class newton_method:

    def __init__(self, max_iterations=1000, tolerance=1e-7, verbose=False):
       
        self.max_iter = max_iterations
        self.tol = tolerance
        self.verbose = verbose

    def solve(self, objective, derivative, initial_point):

        x = initial_point
        for i in range(self.max_iter):

            x -= objective(x)/derivative(x)

            if np.abs(objective(x)) < self.tol:
                if self.verbose:
                    print("iterations:", i+1)
                break

        if self.verbose:
            print("solution:", x)
        return x



class bisection_method:

    def __init__(self, max_iterations=1000, verbose=False):
       
        self.max_iter = max_iterations
        self.verbose = verbose

    def solve(self, objective, initial_bound):

        a = initial_bound[0]
        b = initial_bound[1]

        for i in range(self.max_iter):

            x = (a + b)/2

            if np.linalg.norm(objective(x)) < 1e-10:
                if self.verbose:
                    print("iterations:", i+1)
                break
            elif objective(x)*objective(a) < 0:
                b = x
            else:
                a = x

        if self.verbose:
            print("solution:", x)
        return x



class fix_point_method:

    def __init__(self, max_iterations=1000, tolerance=1e-7, verbose=False):
       
        self.max_iter = max_iterations
        self.tol = tolerance
        self.verbose = verbose

    def solve(self, objective, initial_point):

        x = initial_point

        for i in range(self.max_iter):

            x_k = objective(x)

            step_size = np.linalg.norm(x - x_k)
            if step_size < self.tol:
                if self.verbose:
                    print("iterations:", i+1)
                break

            x = x_k

        if self.verbose:
            print("solution:", x)
        return x
