### Numerical Analysis (Fall 2020), NTNU

def newton_method(function, d_function, x, iters, tol):

    i = 1
    while abs(function(x)) >= tol and i <= iters:
        x = x - function(x)/d_function(x)
        i += 1
    
    return x


def bisection_method(function, a, b, iters, tol):

    c =(a+b)/2
    i = 1

    while abs(b-a) >= tol and abs(function(c)) >= tol and i <= iters:
        
        if function(c) == 0: 
            break
        elif function(c)*function(a) < 0: 
            b = c
        else: 
            a = c

        x = c
        c = (a+b)/2
        i += 1
    
    return x


def fix_point_method(function, x_init, iters, tol):

    x = function(x_init)

    i = 1
    while abs(x-x_init) >= tol and i <= iters:

        temp_root = x
        temp_error = abs(x-x_init)

        x_init = x
        x = function(x_init)
        i += 1

    return temp_root, temp_error