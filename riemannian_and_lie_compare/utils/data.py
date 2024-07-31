import numpy as np
class createToyData:

    def __init__(self, pcd, rot=np.eye(3), t=np.zeros(3)):

        self.rot = rot
        self.t = t

        self.pcd1point = pcd
        self.pcd2point = (self.rot@self.pcd1point.T).T + t