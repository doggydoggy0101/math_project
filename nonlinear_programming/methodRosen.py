import numpy as np
import cvxpy as cp

class gradientProjection:
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

    def binding(self, x, index):
        return np.round(self.coef[index]["A_linear"]@x, 7) == self.coef[index]["b"]

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
        stop = False
        for iteration in range(self.max_iter):
            if self.verbose:
                print("-"*10 + " iteration {} ".format(iteration+1) + "-"*10)
            A1, A2, b2 = [], [], []
            for i in range(len(self.coef)):
                bind = self.binding(x, i)
                if bind:
                    A1.append(self.coef[i]["A_linear"])
                else:
                    A2.append(self.coef[i]["A_linear"])
                    b2.append(self.coef[i]["b"])

            M = np.zeros((len(A1), 2))
            for i in range(len(A1)):
                M[i,:] = A1[i]

            while True:
                if len(M) == 0:
                    if np.round(np.linalg.norm(self.derivative(x)), 7) == 0:
                        stop = True
                        break # stopping criteria
                    else:
                        d = -self.derivative(x)
                        break # break while
                
                P = np.eye(2) - M.T@np.linalg.inv(M@M.T)@M

                d = -P@self.derivative(x)
                if self.verbose:
                    print("direction:", d)

                if np.round(self.derivative(x)@d, 7) == 0:

                    u = -np.linalg.inv(M@M.T)@M@self.derivative(x)
                    if all(u_i >= 0 for u_i in u):
                        stop = True
                        break # stopping criteria
                    else:
                        for i, u_i in enumerate(u):
                            if u_i < 0:
                                M = np.delete(M, i, axis=0)
                                break # break while
                        continue
                else:
                    break 
            if stop:
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

    gradientProjection(initial=initial_point, verbose=True)