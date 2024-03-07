import numpy as np

class check:
    ''' check A - H is in second order cone '''
    def __init__(self, vec_1, vec_2, theta):
        ''' input vector has to be array '''
        self.vec1 = vec_1
        self.vec2 = vec_2
        self.theta = theta

        self.bool = self.checkSOC(self.A() - self.H())

    def spec(self, vec):
        ''' spectral decomposition (not used) '''
        norm = np.linalg.norm(vec[1:])
        lambda_1 = vec[0] - norm*(1/np.tan(self.theta))
        lambda_2 = vec[0] + norm*np.tan(self.theta)

        x_1 = lambda_1*np.sin(self.theta)**2+lambda_2*np.cos(self.theta)**2
        x_2 = (lambda_2-lambda_1)*(np.sin(self.theta)*np.cos(self.theta))*(vec[1:]/norm)

        return np.insert(x_2, 0, x_1, axis=0)

    def spec_inv(self, vec):
        ''' spectral decomposition inverse '''
        norm = np.linalg.norm(vec[1:])
        lambda_1_inv = 1/(vec[0] - norm*(1/np.tan(self.theta)))
        lambda_2_inv = 1/(vec[0] + norm*np.tan(self.theta))

        x_1 = lambda_1_inv*np.sin(self.theta)**2+lambda_2_inv*np.cos(self.theta)**2

        if norm == 0:
            x_2 = np.zeros(len(vec[1:]))
            x_2[0] = 1
        else:
            x_2 = (lambda_2_inv-lambda_1_inv)*(np.sin(self.theta)*np.cos(self.theta))*(vec[1:]/norm)

        return np.insert(x_2, 0, x_1, axis=0)

    def A(self):
        return (self.vec1 + self.vec2)/2

    def H(self):
        return self.spec_inv((self.spec_inv(self.vec1) + self.spec_inv(self.vec2))/2)

    def checkSOC(self, vec):
        ''' check if a vector is in second order cone '''
        if vec[0] + 1e-7 >= np.linalg.norm(vec[1:]):
            return True
        else:
            # print(vec[0] - np.linalg.norm(vec[1:]))
            return False