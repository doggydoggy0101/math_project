### Computer Programming (Spring 2019), NTNU

import numpy as np

def Gaussian_elimination(A, B):

    n = B.size
    M = np.hstack([A,B]) #augmented matrix
    X = np.zeros((n,1),dtype=float)

    check = True
    for kk in np.arange(0,n):

        pivot=np.array(abs(M[kk:n,kk]))
        Max_pivot=max(pivot)
        Max_row=np.where(pivot==Max_pivot)+kk

        if Max_row != kk:
            temp = np.array(M[kk,:])
            M[kk,:] = M[Max_row,:]
            M[Max_row,:] = temp
        
        if Max_pivot == 0:
            print("Matrix is singular.")
            check = False
            break

        t = M[kk+1:n,kk] / M[kk,kk]
        ts= np.size(t)
        tt= t.reshape((ts,1)) # transpose

        M[kk+1:n,kk]=0
        M[kk+1:n,kk+1:n+1] = M[kk+1:n,kk+1:n+1] - np.dot(tt,[M[kk,kk+1:n+1]])

    # Backward Substitution
    m = n-1 # python starts with 0
    if check == True:
        X[m] = M[m,n] / M[m,m] 
        for ii in np.arange(m-1,-1,-1):
            X[ii] = (M[ii,n] - np.dot(M[ii,ii+1:n],X[ii+1:n])) / M[ii,ii]       

    return X