import numpy as np 
from fractions import Fraction
np.set_printoptions(formatter={'all':lambda x: str(Fraction(x).limit_denominator())})
from simplex import simplex_iteration

# Ex 
#     -6x1     +x3 -2x4 +2x5 =6
#     -3x1 +x2     +6x4 +3x5 =15
#      5x1         +3x4 -2x5 =-21

X = np.array([[ -6,  0,  1, -2,  2,  6],
              [ -3,  1,  0,  6,  3, 15],
              [  5,  0,  0,  3, -2,-21]], dtype=float)

# Ex 
#     -2x1      +6x3 +2x4      -3x6 + x7 =20
#     -4x1 + x2 +7x3 + x4      - x6      =10
#     -5x3           +3x4 + x5 - x6      =60
#     13x3           -6x4      +2x6      =110

X = np.array([[ -2,  0,  6,  2,  0, -3,  1, 20],
              [ -4,  1,  7,  1,  0, -1,  0, 10],
              [  0,  0, -5,  3,  1, -1,  0, 60],
              [  0,  0, 13, -6,  0,  2,  0,110]], dtype=float)


simplex_iteration(X)


# linear equation system:
# -2.0x1 +6.0x3 +2.0x4 -3.0x6 +1.0x7 =20.0
# -4.0x1 +1.0x2 +7.0x3 +1.0x4 -1.0x6 =10.0
# -5.0x3 +3.0x4 +1.0x5 -1.0x6 =60.0
# 13.0x3 -6.0x4 +2.0x6 =110.0

# --------------------------------------------------

# 1 iteration:
# [[6 -2 -8 0 0 -1 1 0]
#  [-4 1 7 1 0 -1 0 10]
#  [12 -3 -26 0 1 2 0 30]
#  [-24 6 55 0 0 -4 0 170]]

# 2 iteration:
# [[1 -1/3 -4/3 0 0 -1/6 1/6 0]
#  [0 -1/3 5/3 1 0 -5/3 2/3 10]
#  [0 1 -10 0 1 4 -2 30]
#  [0 -2 23 0 0 -8 4 170]]

# 3 iteration:
# [[1 -7/24 -7/4 0 1/24 0 1/12 5/4]
#  [0 1/12 -5/2 1 5/12 0 -1/6 45/2]
#  [0 1/4 -5/2 0 1/4 1 -1/2 15/2]
#  [0 0 3 0 2 0 0 230]]

# --------------------------------------------------

# iterations: 3
# basic variables (index): [1 4 6]
# basic feasible solution: [5/4 0 0 45/2 0 15/2 0]
# minimize: -230.0