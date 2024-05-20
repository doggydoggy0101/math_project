import numpy as np
import cvxpy as cp
class linearZoutendijk:
    def __init__(self, initial, max_iter=1000, verbose=False):
        self.max_iter = max_iter
        self.verbose = verbose

        self.quad = np.array([[2, -1], [-1, 2]])
        self.linear =  np.array([-4, -6])
        self.coef = [{"A_linear" : np.array([1, 1]), "b" : 2}, 
                     {"A_linear" : np.array([1, 5]), "b" : 5},
                     {"A_linear" : np.array([-1, 0]), "b" : 0},
                     {"A_linear" : np.array([0, -1]), "b" : 0}]
        self.run(initial)

    def objective(self, x):
        return x@self.quad@x + self.linear@x
    
    def derivative(self, x):
        return 2*self.quad@x + self.linear

    def constraint(self, x, index):
        val = self.coef[index]["A_linear"]@x
        return val, np.round(val, 7) == self.coef[index]["b"]

    def lambda_max(self, x, d, A2, b2):
        f = b2 - A2@x
        h = A2@d
        l_max = 1e+10
        for i, h_i in enumerate(h):
            if h_i > 0:
                l_i = f[i]/h[i]
                if l_i <= l_max:
                    l_max = l_i
        return l_max

    def run(self, x):
        for iteration in range(self.max_iter):
            if self.verbose:
                print("-"*10 + " iteration {} ".format(iteration+1) + "-"*10)
            A1, A2, b2 = [], [], []
            for i in range(len(self.coef)):
                val, bind = self.constraint(x, i)
                if bind:
                    A1.append(self.coef[i]["A_linear"])
                else:
                    A2.append(self.coef[i]["A_linear"])
                    b2.append(self.coef[i]["b"])

            # linear programming
            d = cp.Variable(2)
            constraints = [np.array(A1)@d <= np.zeros(2)]
            for i in range(2):
                constraints += [-1 <= d[i]]
                constraints += [d[i] <= 1]
            prob = cp.Problem(cp.Minimize(np.array(self.derivative(x)).T@d), constraints)
            prob.solve()
            d = d.value
            if self.verbose:
                print("direction:", d)

            # stopping criteria
            if np.round(self.derivative(x)@d, 7) == 0:
                break

            # line search
            l = cp.Variable(1)
            constraints = [0 <= l]
            constraints += [l <= self.lambda_max(x, d, np.array(A2), np.array(b2))]
            prob = cp.Problem(cp.Minimize((d@self.quad@d)*l**2 + (2*d@self.quad@x + self.linear@d)*l), constraints)
            prob.solve()
            l = l.value
            if self.verbose:
                print("lambda:", l)

            x = x + l*d
            if self.verbose:
                print("x:", x)

        self.optimal_sol = x
        self.optimal_val = self.objective(self.optimal_sol)

        if self.verbose:
            print("-"*10 + " result " + "-"*10)
            print("optimal solution:", self.optimal_sol)
            print("optimal value:", self.optimal_val)



if __name__ == "__main__":

    initial_point = np.array([0.0, 0.0])

    linearZoutendijk(initial=initial_point, verbose=True)