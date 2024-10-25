function [sol, flag, RelRes, ITER] = bicg_method(shift_L, b, tol, maxit, prec_M1, prec_M2)

    if (nargin == 4)
        [sol, flag, RelRes, ITER] = bicg(shift_L, b, tol, maxit);
    elseif (nargin == 5)
        [sol, flag, RelRes, ITER] = bicg(shift_L, b, tol, maxit, prec_M1);
    elseif (nargin == 6)
        [sol, flag, RelRes, ITER] = bicg(shift_L, b, tol, maxit, prec_M1, prec_M2);
    else
        fprintf("input variables eror")
    end
end