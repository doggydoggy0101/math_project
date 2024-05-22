import numpy as np
import cvxpy as cp

class reduceGradient:
    def __init__(self, initial, max_iter=1000, verbose=False):
        self.max_iter = max_iter
        self.verbose = verbose

        self.quad = np.array([[2, -1, 0, 0], [-1, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.linear =  np.array([-4, -6, 0, 0])
        # self.coef = [{"A_linear" : np.array([1, 1, 1, 0]), "b" : 2}, 
        #              {"A_linear" : np.array([1, 5, 0, 1]), "b" : 5}]
        self.A = np.array([[1, 1, 1, 0], [1, 5, 0, 1]])
        self.b = np.array([2, 5])
        self.run(initial)

    def objective(self, x):
        return x@self.quad@x + self.linear@x
    
    def derivative(self, x):
        return 2*self.quad@x + self.linear

    def binding(self, x, index):
        return np.round(self.coef[index]["A_linear"]@x, 7) == self.coef[index]["b"]

    def lambda_max(self, x, d):

        l_max = 1e+10

        if not all(d_i > 0 for d_i in d):
            for i, d_i in enumerate(d):
                if d_i < 0:
                    l_i = -x[i]/d[i]
                    if l_i < l_max:
                        l_max = l_i
        return l_max

    def run(self, x):

        for iteration in range(self.max_iter):
            if self.verbose:
                print("-"*10 + " iteration {} ".format(iteration+1) + "-"*10)

            dummy = x.copy()
            index_set = []
            for i in range(self.A.shape[0]):
                index_set.append(np.argmax(dummy))
                dummy[index_set[-1]] = -1e+10
            index_set.sort()

            index_set_perp = []
            for i in range(self.A.shape[1]):
                if i not in index_set:
                    index_set_perp.append(i)

            B = np.eye(self.A.shape[0])
            for b_i, a_i in enumerate(index_set):
                B[:, b_i] = self.A[:, a_i]

            N = np.zeros((self.A.shape[0], self.A.shape[1]-self.A.shape[0]))
            for n_i, a_i in enumerate(index_set_perp):
                N[:, n_i] = self.A[:, a_i]

            gradB = self.derivative(x)[index_set]
            r = self.derivative(x) - gradB.T@np.linalg.inv(B)@self.A

            print("B:\n", B)
            print("N:\n", N)
            print("gradB:", gradB)
            print("r:", r)

            dN = np.zeros(len(index_set_perp))
            for i, r_i in enumerate(index_set_perp):
                if r[r_i] > 0:
                    dN[i] = -x[r_i]*r[r_i]
                else:
                    dN[i] = -r[r_i]
            dB = -np.linalg.inv(B)@N@dN

            d = np.zeros(len(x))
            d[index_set] = dB
            d[index_set_perp] = dN

            if self.verbose:
                print("direction:", d)

            # stopping criteria
            if np.round(self.derivative(x)@d, 7) == 0:
                break

            # line search
            l = cp.Variable(1)
            constraints = [0 <= l]
            constraints += [l <= self.lambda_max(x, d)]
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

    initial_point = np.array([0.0, 0.0, 2.0, 5.0])

    reduceGradient(initial=initial_point, verbose=True)