import numpy as np 

def simplex_iteration(X):

    m = X.shape[0] - 1
    n = X.shape[1] - 1

    print("linear equation system:")
    for row in range(m+1):
        text = ""
        for i in range(n):
            if X[row, i] != 0:
                text_i = "+" + str(X[row, i]) + "x" + str(i+1) + " " if text != "" and X[row, i] > 0 else str(X[row, i]) + "x" + str(i+1) + " "
                text += text_i
        text_i = "=" + str(X[row, n])
        text += text_i
        print(text)
    print("\n" + "-"*50)

    F = np.zeros(n) # 給 basic feasible sol空間
    label = np.zeros(m) # 給 table左邊那排 label空間
    tt = 0 # 係數為正的數量
    num = 0 # 跌代次數
    while tt != n:

        tlabel=0
        tt=0 # 係數為正的數量

        # 找basic variable當label
        for j in np.arange(m):
            for i in np.arange(n):
                if X[j][i]==1 and np.sum(X[:,i])==1:
                    label[j]=i+1

        mlabel=np.array([]) # 係數為負
        for t in np.arange(n):
            if X[m,t] >= 0:
                tt=tt+1
            else:
                mlabel=np.append(mlabel, t)

        if tt ==n: # 全部係數都為正 print答案
            sol=X[m,n]
            
            for f in np.arange(m):
                ff=int(label[f]-1)
                F[ff]=X[f,n]
            
            print("\n" + "-"*50 +"\n")
            print("iterations:",str(num))
            print("basic variables (index):", str(label))
            print("basic feasible solution:", str(F))
            print("minimize:", str(-sol))
            break

        # 找目標含數裡係數負的 min 得出pivoting column
        M=np.array([])
        for mm in np.arange(len(mlabel)):
            M=np.append(M,X[m,int(mlabel[mm])])

        M=np.min(M)

        for mmm in np.arange(n):
            if X[m,mmm]==M:
                ttt=mmm 
        
        tlabel=ttt # column

        # 找column上面係數為正
        Bb=np.array([])
        for k in np.arange(m):
            if X[k,tlabel]>0:
                Bb=np.append(Bb,k)

        # 找column上面係數為正 且 b/a的 min
        B=np.array([])

        for kk in np.arange(len(Bb)):
            bbb=int(Bb[kk])
            B=np.append(B,X[bbb,n]/X[bbb,tlabel])

        B=np.min(B)   
        for kkk in np.arange(m):   
            if X[kkk,n]/X[kkk,tlabel]==B:
                ll=kkk # ll是pivot row

        label[ll]=tlabel+1 # tlabel是column

        # pivot係數變1
        if X[ll,tlabel] !=1:
            X[ll,:]=X[ll,:]/X[ll,tlabel]

        # pivot其他變0
        Xtemp = X[ll,:].copy()
        for kkkk in np.arange(m+1):
            X[kkkk,:]=X[kkkk,:]-X[kkkk,tlabel]*Xtemp
        X[ll,:]=Xtemp

        print("\n{} iteration:".format(num+1))
        print(X) 
        num += 1