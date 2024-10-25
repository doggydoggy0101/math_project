import numpy as np 

class Simplex:
    def __init__(self, CanonicalForm, verbose=True):

        self.X = CanonicalForm
        self.verbose = verbose

        self.m = self.X.shape[0] - 1
        self.n = self.X.shape[1] - 1

        if self.verbose: 
            self.dispEquation()

    def dispEquation(self):

        print("\n" + "-"*13 + " Linear Equation System " + "-"*14)
        for row in range(self.m + 1):
            text = ""
            for i in range(self.n):
                if self.X[row, i] != 0:
                    if text != "" and self.X[row, i] > 0:
                        text_i = "+" + "x" + str(i+1) + " " if self.X[row, i] == 1 else "+" + str(self.X[row, i]) + "*x" + str(i+1) + " "
                    else:
                        text_i = "x" + str(i+1) + " " if self.X[row, i] == 1 else str(self.X[row, i]) + "*x" + str(i+1) + " "
                    text += text_i
            text_i = "=" + str(self.X[row, self.n])
            text += text_i
            print(text)

    def dispSol(self):
        
        print("\n" + "-"*21 + " Summary " + "-"*21)
        print("iterations:",str(self.iters))
        print("basic variables (index):", str(self.label))
        print("basic feasible solution:", str(self.sol_set))
        print("optimal:", str(-self.sol))

    def dispIter(self):

        print("initial system:") if self.iters == 0 else print("\n{} iteration:".format(self.iters))
        print(self.X) 


    def solve(self): 
        if self.verbose: 
            print("\n" + "-"*20 + " Iteration " + "-"*20)

        self.label = np.zeros(self.m) # basic variable label
        self.iters = 0 # num of iterations
        basic_var = 0 # num of basic varialbes

        while basic_var != self.n:

            if self.verbose: 
                self.dispIter()

            # set pivot points as basic variable 
            for i in range(self.m):
                for j in range(self.n):
                    if self.X[i][j] == 1 and np.sum(self.X[:,j]) == 1:
                        self.label[i] = j+1

            # compute positive and negative coefficient
            basic_var = 0 # num of nonnegative basic variables
            neg_label = [] # negative coefficient
            for j in range(self.n):
                if self.X[self.m, j] >= 0:
                    basic_var += 1
                else:
                    neg_label.append(j)

            # all labels are nonnegative, return solution
            if basic_var == self.n:

                self.sol = self.X[self.m, self.n] 
                self.sol_set = np.zeros(self.n) # basic feasible sol

                for i in range(self.m):
                    basic_var_idx = int(self.label[i]-1)
                    self.sol_set[basic_var_idx] = self.X[i, self.n]
                break

            ### simplex iteration

            # choose the smallest nonnegative coefficient
            neg_coef_min = 0
            for neg_idx in range(len(neg_label)):
                neg_coef = self.X[self.m,int(neg_label[neg_idx])]
                if neg_coef < neg_coef_min:
                    neg_coef_min = neg_coef

            # get pivoting variable column
            pivot_col = np.where(self.X[self.m,:] == neg_coef_min)[0][0]

            # get pivoting variable row
            ratio_min = 1e+7
            for i in range(self.m):
                if self.X[i, pivot_col] > 0:
                    ratio = self.X[i, self.n] / self.X[i, pivot_col]
                    if ratio < ratio_min:
                        ratio_min = ratio
                        pivot_row = i

            # update basic variable label
            self.label[pivot_row] = pivot_col + 1

            # pivoting
            if self.X[pivot_row, pivot_col] != 1:
                self.X[pivot_row, :] = self.X[pivot_row, :] / self.X[pivot_row, pivot_col]

            temp = self.X[pivot_row, :].copy()
            for i in range(self.m+1):
                self.X[i,:] -= self.X[i, pivot_col]*temp
            self.X[pivot_row, :] = temp

            self.iters+=1

        if self.verbose: 
            self.dispSol()