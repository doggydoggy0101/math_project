import numpy as np
import cvxpy as cp

class nonlinearTopkisVeinott:
    def __init__(self, initial, max_iter=1000):
        self.max_iter = max_iter
        self.quad = np.array([[2, -1], [-1, 2]])
        self.linear =  np.array([-4, -6])
        self.coef = [{"g_quad" : np.zeros((2, 2)), "g_linear" : np.array([1, 5]), "g_const" : -5},
                     {"g_quad" : np.array([[2, 0], [0, 0]]), "g_linear" : np.array([0, -1]), "g_const" : 0},
                     {"g_quad" : np.zeros((2, 2)), "g_linear" : np.array([-1, 0]), "g_const" : 0},
                     {"g_quad" : np.zeros((2, 2)), "g_linear" : np.array([0, -1]), "g_const" : 0}]
        self.run(np.array(initial))

    def objective(self, x):
        return x@self.quad@x + self.linear@x
    
    def derivative(self, x):
        return 2*self.quad@x + self.linear

    def constraint(self, x, index):
        val = x@self.coef[index]["g_quad"]@x + self.coef[index]["g_linear"]@x + self.coef[index]["g_const"]
        return val, np.round(val, 7) == 0

    def lambda_max(self, x, d):
        l_max = cp.Variable(1)
        constraints = [l_max >= 0]
        for coef in self.coef:
            a = d@coef["g_quad"]@d
            b = 2*d@coef["g_quad"]@x + coef["g_linear"]@d
            c = x@coef["g_quad"]@x + coef["g_linear"]@x + coef["g_const"]
            constraints += [a*l_max**2 + b*l_max + c <= 0]
        prob = cp.Problem(cp.Maximize(l_max), constraints)
        prob.solve()
        l_max = l_max.value
        return l_max

    def run(self, x):
        ''' CVXPY '''
        for iteration in range(self.max_iter):
            print("-"*10 + " iteration {} ".format(iteration+1) + "-"*10)

            # linear programming
            z, d = cp.Variable(1), cp.Variable(2)
            constraints = [np.array(self.derivative(x))@d - z <= 0]
            for g in self.coef:
                constraints += [(2*g["g_quad"]@x + g["g_linear"])@d + x@g["g_quad"]@x + g["g_linear"]@x + g["g_const"] - z <= 0]
            for i in range(2):
                constraints += [-1 <= d[i]]
                constraints += [d[i] <= 1]
            prob = cp.Problem(cp.Minimize(z), constraints)
            prob.solve()
            z, d = z.value,  d.value
            print("z:", z)
            print("direction:", d)

            # stopping criteria
            if np.round(z, 7) == 0:
                break

            # line search
            l = cp.Variable(1)
            constraints = [0 <= l]
            constraints += [l <= self.lambda_max(x, d)]
            prob = cp.Problem(cp.Minimize((d@self.quad@d)*l**2 + (2*d@self.quad@x + self.linear@d)*l), constraints)
            prob.solve()
            l = l.value
            print("lambda:", l)

            x = x + l*d
            print("x:", x)
            print("f(x):", self.objective(x))

        print("-"*10 + " result " + "-"*10)
        print("optimal solution:", x)
        print("optimal value:", self.objective(x))




from fractions import Fraction
np.set_printoptions(formatter={'all':lambda x: str(Fraction(x).limit_denominator())})

def main():
    ''' Example 10.2.4 '''
    initial_point = np.array([0.0, 0.75])
    max_iteration = 5

    nonlinearTopkisVeinott(initial=initial_point, max_iter=max_iteration)

main()