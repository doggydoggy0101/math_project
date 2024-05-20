import numpy as np
import cvxpy as cp

class penaltySuccessiveLP:
    def __init__(self, initial, delta, max_iter=1000, verbose=False):
        self.max_iter = max_iter
        self.verbose = verbose

        self.mu = 10

        self.f_quad = np.array([[2, -1], [-1, 2]])
        self.f_linear =  np.array([-4, -6])

        self.g_quad = np.array([[2, 0], [0, 0]])
        self.g_linear =  np.array([0, -1])

        self.coef = [{"A_linear" : np.array([1, 5]), "A_const" : -5},
                     {"A_linear" : np.array([-1, 0]), "A_const" : 0},
                     {"A_linear" : np.array([0, -1]), "A_const" : 0}]

        self.run(initial, delta)

    def objective(self, x):
        return x@self.f_quad@x + self.f_linear@x

    def linear_penalty(self, x):
        return x@self.f_quad@x + self.f_linear@x + self.mu*max(0, x@self.g_quad@x + self.g_linear@x)

    def linear_approx(self, x, d):
        return x@self.f_quad@x + self.f_linear@x + (2*self.f_quad@x + self.f_linear)@d + self.mu*max(0, x@self.g_quad@x + self.g_linear@x + (2*self.g_quad@x + self.g_linear)@d)


    def linear_programming(self, x, delta):
        d, y = cp.Variable(2), cp.Variable(1)
        obj = (2*self.f_quad@x + self.f_linear)@d + self.mu*y
        constraints = [y >= 0]
        constraints += [y >= x@self.g_quad@x + self.g_linear@x + (2*self.g_quad@x + self.g_linear)@d]
        for i in range(len(self.coef)):
            constraints += [self.coef[i]["A_linear"]@(x + d) + self.coef[i]["A_const"] <= 0]
        for i in range(2):
            constraints += [-delta[i] <= d[i]]
            constraints += [d[i] <= delta[i]]
        prob = cp.Problem(cp.Minimize(obj), constraints)
        prob.solve()
        d = d.value
        return d

    def trust_region(self, ratio, delta):

        if ratio < self.r0:
            delta *= self.beta
            if self.verbose:
                print("=== reject above solution ===")
            return False, delta
        else:
            if ratio < self.r1:
                delta *= self.beta
            if ratio > self.r2:
                delta /= self.beta
            return True, delta


    def run(self, x, delta):

        self.r0 = 1e-6
        self.r1 = 0.25
        self.r2 = 0.75
        self.beta = 0.5

        if self.verbose:
            print("-"*10 + " iteration 1" + "-"*10)
        for iteration in range(self.max_iter):
            if self.verbose:
                print("solving with trust-region {}".format(delta))

            # linear programming
            d = self.linear_programming(x, delta)
            if self.verbose:
                print("direction:", d)
                print("x:", x)

            delta_penalty = self.linear_penalty(x) - self.linear_penalty(x + d)
            delta_approx = self.linear_approx(x, np.zeros(len(x))) - self.linear_approx(x, d) 

            # stopping criteria
            if np.round(delta_approx, 7) == 0:
                self.optimal_sol = x
                self.optimal_val = self.objective(self.optimal_sol)
                if self.verbose:
                    print("-"*10 + " result " + "-"*10)
                    print("optimal solution:", self.optimal_sol)
                    print("optimal value:", self.optimal_val)
                break

            # trust-region
            ratio = delta_penalty / delta_approx
            if self.verbose:
                print("ratio:", ratio)
            check, delta = self.trust_region(ratio, delta)
            if check:
                x = x + d
                if self.verbose:
                    print("-"*10 + " iteration {} ".format(iteration+1) + "-"*10)
                    


if __name__ == "__main__":
    
    initial_point = np.array([0.0, 1.0])
    initial_bound = np.array([1.0, 1.0])
    max_iteration = 1000

    penaltySuccessiveLP(initial=initial_point, delta=initial_bound, max_iter=max_iteration, verbose=True)