### Numerical Analysis (Fall 2020), NTNU

import numpy as np
import sympy as sp

from root_find import newton_method, bisection_method, fix_point_method
from linear_solver import Gaussian_elimination

sym_x = sp.Symbol("x")
verbose = True

def f(x): 
    return x**2 - 2 

def df(x): 
    return 2*x

print("\nroot finding function:", f(sym_x))

print("="*3 + " solved by Newton's method " + "="*3)
model = newton_method(verbose=verbose)
model.solve(f, df, initial_point=1)

print("="*3 + " solved by bisection method " + "="*3)
model = bisection_method(verbose=verbose)
model.solve(f, initial_bound=[1, 4])



def g(x): 
    return (3*x**2 + 3)**(1/4)

print("\nfix point finding function:", g(sym_x))

print("="*3 + " solved by fix point method " + "="*3)
model = fix_point_method(verbose=verbose)
model.solve(g, initial_point=1)



A = np.array([[1, -2, 3],
              [2, 1, -3],
              [3, -1, 2]]) 
b = np.array([5, -3, 6]).reshape((3, 1))

print("\nlinear system Ax=b:")
print("A:\n", A)
print("b:", b.ravel())

model = Gaussian_elimination(A, b, verbose=True)
model.solve()