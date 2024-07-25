from rootfind import newton_method
verbose = True

def f(x): 
    return x**2 - 2 

def df(x): 
    return 2*x

model = newton_method(verbose=verbose)
model.solve(f, df, initial_point=1)
        