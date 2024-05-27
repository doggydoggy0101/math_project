import numpy as np
import scipy as sp

def als(A, k, num_iter, init_W = None, init_H = None):
	'''
	Run the alternating least squares method to perform nonnegative matrix factorization on A.
	Return matrices W, H such that A = WH.
	
	Parameters:
		A: ndarray
			- m by n matrix to factorize
		k: int
			- integer specifying the column length of W / the row length of H
			- the resulting matrices W, H will have sizes of m by k and k by n, respectively
		num_iter: int
			- number of iterations for the multiplicative updates algorithm

	Returns:
		W: ndarray
			- m by k matrix where k = dim
		H: ndarray
			- k by n matrix where k = dim
	'''

	if init_W is None:
		W = np.random.rand(np.size(A, 0), k)
	else:
		W = init_W

	if init_H is None:
		H = np.random.rand(k, np.size(A, 1))
	else:
		H = init_H

	for i in range(num_iter):

		H = sp.linalg.lstsq(W, A)[0]
		H[H < 0] = 0

		W = sp.linalg.lstsq(H.T, A.T)[0].T
		W[W < 0] = 0

	return W.astype(np.float32), H.astype(np.float32)