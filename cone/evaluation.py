import numpy as np

class check_AH:
    ''' check A - H is in second order cone '''
    def __init__(self, vec_1, vec_2, theta, verbose=False):
        ''' input vector has to be array '''
        self.vec1 = vec_1
        self.vec2 = vec_2
        self.theta = theta
        self.verbose = verbose

        if self.verbose:
            print("vector 1:", self.vec1)
            print("vector 2:", self.vec2)
            print("-"*50)
            self.check_circular(self.vec1, "vector 1")
            self.check_circular(self.vec2, "vector 2")

        self.A = self.A_mean()
        self.H = self.H_mean()
        self.bool = self.check_circular(self.A - self.H, "A-H")

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
            w = np.zeros(len(vec[1:]))
            w[0] = 1
            x_2 = (lambda_2_inv-lambda_1_inv)*(np.sin(self.theta)*np.cos(self.theta))*w
        else:
            x_2 = (lambda_2_inv-lambda_1_inv)*(np.sin(self.theta)*np.cos(self.theta))*(vec[1:]/norm)

        return np.insert(x_2, 0, x_1, axis=0)

    def A_mean(self):
        return (self.vec1 + self.vec2)/2

    def H_mean(self):
        return self.spec_inv((self.spec_inv(self.vec1) + self.spec_inv(self.vec2))/2)

    def check_circular(self, vec, name=None):
        ''' check if a vector is in circular cone '''
        if vec[0] + 1e-7 >= np.linalg.norm(vec[1:])*(1/np.tan(self.theta)):
            if self.verbose:
                print(name, "is in circular cone with theta {} deg".format(np.round(self.theta*(180/np.pi),2)))
            return True
        else:
            if self.verbose:
                print("-"*50)
                print(name, "is not in circular cone with theta {} deg".format(np.round(self.theta*(180/np.pi),2)))
                print("x1=", vec[0])
                print("||x2||=", np.linalg.norm(vec[1:]))
                print("x1 < ||x2||")
            return False

class check:
    ''' check if all points satisfies function check_AH '''
    def __init__(self, vec, theta, verbose=False):

        print("circular cone with angle {} deg".format(np.round(theta*(180/np.pi),2)))
        print("checking...")

        self.vec = vec
        self.theta = theta
        self.verbose = verbose

        self.n = self.vec.shape[0] # number of points in cone
        self.false_idx = self.run()

        if len(self.false_idx) == 0:
            print("Certified!")
        else:
            print("Not certified.")

    def run(self):
        point_idx = []
        for i in range(self.n):
            for j in range(i, self.n):
                vec_1 = self.vec[i]
                vec_2 = self.vec[j]
                if check_AH(vec_1, vec_2, self.theta).bool:
                    pass
                else:
                    if self.verbose:
                        print("found case not in SOC")
                        print(i,j)
                    point_idx.append([i,j])
        return point_idx