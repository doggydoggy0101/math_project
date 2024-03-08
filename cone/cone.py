import numpy as np
import matplotlib.pyplot as plt

class CircularCone3D:
    ''' Make a 3D circular cone given a fixed cube boundary, number of points, and angle theta,
        where x_1=z in R and x_2=[x,y] in R^2. '''
    def __init__(self, boundary, number, theta, verbose=False):

        self.bdd = boundary
        self.num = number
        self.theta = theta
        self.verbose = verbose

        x_, y_, z_ = self.makeMesh()
        self.x, self.y, self.z = self.makeCone(x_, y_, z_)

        if self.verbose:
            self.plotCone()

    def makeMesh(self):
        ''' returns vectorize meshgirds '''
        u = np.linspace(-self.bdd, self.bdd, self.num)
        v = np.linspace(-self.bdd, self.bdd, self.num)
        w = np.linspace(0, self.bdd, self.num//2)

        x,y,z = np.meshgrid(u,v,w)

        return x.ravel(), y.ravel(), z.ravel() # vectorize

    def makeCone(self, x,y,z):
        ''' returns the interior of circular cone '''
        Lx,Ly,Lz = [],[],[]
        for i in range(self.num**2*(self.num//2)):
            if z[i] - np.linalg.norm([x[i],y[i]])*(1/np.tan(self.theta)) > 1e-7:
                Lx.append(x[i])
                Ly.append(y[i])
                Lz.append(z[i])
        
        return np.array(Lx), np.array(Ly), np.array(Lz)
        
    def plotCone(self, size=2, color="#2980B9"):
        
        fig = plt.figure( figsize=(6,5), dpi=120)
        ax = plt.axes(projection='3d')
        ax.scatter3D(self.x, self.y, self.z, s=size, c=color)

        ax.set_xlim(-self.bdd, self.bdd)
        ax.set_ylim(-self.bdd, self.bdd)
        ax.set_zlim(0, self.bdd)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_title("Circular Cone: " + r"$(z,x,y)\in\mathbb{R}\times\mathbb{R}^2$")
        plt.show()

    def plotPoint(self, points, size=2, color="#2980B9"):

        fig = plt.figure( figsize=(6,5), dpi=120)
        ax = plt.axes(projection='3d')
        ax.scatter3D(self.x, self.y, self.z, s=1, c=color, alpha=0.2)

        if len(points.shape) == 1:
            ax.scatter3D(points[0], points[1], points[2], s=size, c='r')
        else:
            ax.scatter3D(points[:,0], points[:,1], points[:,2], s=size, c='r')
            
        ax.set_xlim(-self.bdd, self.bdd)
        ax.set_ylim(-self.bdd, self.bdd)
        ax.set_zlim(0, self.bdd)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_title("Circular Cone: " + r"$(z,x,y)\in\mathbb{R}\times\mathbb{R}^2$")
        plt.show()
