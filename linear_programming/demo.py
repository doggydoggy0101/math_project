import numpy as np 
from simplex import Simplex

# for better display
from fractions import Fraction
np.set_printoptions(formatter={'all':lambda x: str(Fraction(x).limit_denominator())})

class CanonicalForm:

    def __init__(self):

        self.ex1 = np.array([[1, 0, 5/3, -5/3,  5],
                             [0, 1, 1/3,  8/3,  1],
                             [0, 0, 3/2, -2/3, -4]])

        self.ex2 = np.array([[ -6,  0,  1, -2,  2,  6],
                             [ -3,  1,  0,  6,  3, 15],
                             [  5,  0,  0,  3, -2,-21]], dtype=float)

        self.ex3 = np.array([[  3,  2,  0,  1,  0,  0, 60],
                             [ -1,  1,  4,  0,  1,  0, 10],
                             [  2, -2,  5,  0,  0,  1, 50],
                             [ -2, -3, -3,  0,  0,  0,  0]], dtype=float)

        self.ex4 = np.array([[  1,  2, -2,  1,  0,  0, 1],
                             [  2, -1,  3,  0,  1,  0, 4],
                             [  1,  1,  5,  0,  0,  1, 2],
                             [ -1,  2, -3,  0,  0,  0, 0]], dtype=float)


problem = CanonicalForm().ex4
Simplex(CanonicalForm=problem, verbose=True).solve()
