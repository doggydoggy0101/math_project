import numpy as np 
from fractions import Fraction
np.set_printoptions(formatter={'all':lambda x: str(Fraction(x).limit_denominator())})
from simplex import Simplex

# Ex 
#     -6x1     +x3 -2x4 +2x5 =6
#     -3x1 +x2     +6x4 +3x5 =15
#      5x1         +3x4 -2x5 =-21

X = np.array([[ -6,  0,  1, -2,  2,  6],
              [ -3,  1,  0,  6,  3, 15],
              [  5,  0,  0,  3, -2,-21]], dtype=float)

# Ex 
#      3x1 + 2x2       + x4           =60
#      -x1 +  x2 + 4x3      + x5      =10
#      2x1 - 2x2 + 5x3           + x6 =50
#     -2x1 - 3x2 - 3x3                = 0

X = np.array([[  3,  2,  0,  1,  0,  0, 60],
              [ -1,  1,  4,  0,  1,  0, 10],
              [  2, -2,  5,  0,  0,  1, 50],
              [ -2, -3, -3,  0,  0,  0,  0]], dtype=float)

sol = Simplex(CanonicalForm=X, verbose=True)
sol.iterate()