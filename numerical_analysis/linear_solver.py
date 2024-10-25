import numpy as np

class Gaussian_elimination:

    def __init__(self, A, b, verbose=False):
        """ solve Ax=b """
        self.A = A
        self.b = b
        self.verbose = verbose

    def solve(self):

        n = self.b.shape[0]
        M = np.hstack([self.A, self.b]) # augmented matrix
        x = np.zeros((n, 1))

        for i in range(n):

            pivot = np.array(np.abs(M[i:n, i]))
            max_pivot = np.max(pivot)
            max_row = np.where(pivot == max_pivot)[0][0] + i

            if max_row != i:
                temp = np.array(M[i, :])
                M[i, :] = M[max_row, :]
                M[max_row, :] = temp
            
            assert max_pivot != 0, "matrix is singular"

            t = M[i+1:n, i]/M[i, i]
            ts = np.size(t)
            tt = t.reshape((ts, 1)) # transpose

            M[i+1:n, i] = 0
            M[i+1:n, i+1:n+1] = M[i+1:n, i+1:n+1] - np.dot(tt, [M[i, i+1:n+1]])

        # backward substitution
        m = n - 1 
        x[m] = M[m, n]/M[m,m] 
        for j in np.arange(m-1, -1, -1):
            x[j] = (M[j, n] - np.dot(M[j, j+1:n], x[j+1:n]))/M[j ,j]       

        if self.verbose:
            print("solution:\n", x.ravel())
            print("error:", np.linalg.norm(self.A@x - self.b))
        return x