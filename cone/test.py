import numpy as np
from cone import CircularCone3D
from evaluation import check

bdd = 5
num = 20
theta = np.pi/4

cone = CircularCone3D(boundary=bdd, number=num, theta=theta)
points = np.vstack([cone.z, cone.x, cone.y]).T # x_1=z in R and x_2=[x,y] in R^2

check(points, theta)