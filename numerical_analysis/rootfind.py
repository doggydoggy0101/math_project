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
            print("solved by Newton's method:", x)
        return x

