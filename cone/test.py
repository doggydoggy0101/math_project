import numpy as np
from cone import CircularCone3D
from evaluation import check

bdd = 5
num = 20
theta = np.pi/4

cone = CircularCone3D(boundary=bdd, number=num, theta=theta)
x,y,z = cone.x, cone.y, cone.z # x_1=z in R and x_2=[x,y] in R^2
n = x.shape[0] # number of points in cone

breaker = False
point_idx = []
for i in range(n):
    for j in range(i, n):
        vec_1 = np.array([z[i], x[i], y[i]])
        vec_2 = np.array([z[j], x[j], y[j]])

        if check(vec_1, vec_2, theta).bool:
            pass
        else:
            print("found case not in SOC")
            print(i,j)
            point_idx.append([i,j])
            breaker = True
            break
    if breaker:
        break