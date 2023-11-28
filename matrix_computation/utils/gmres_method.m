function [sol, flag, RelRes, ITER] = gmres_method(shift_L, b, tol, maxit, prec_M1, prec_M2)

    if (nargin == 4)
        [sol, flag, RelRes, ITER] = gmres(shift_L, b, 100, tol, maxit);
    elseif (nargin == 5)
        [sol, flag, RelRes, ITER] = gmres(shift_L, b, 100, tol, maxit, prec_M1);
    elseif (nargin == 6)
        [sol, flag, RelRes, ITER] = gmres(shift_L, b, 100, tol, maxit, prec_M1, prec_M2);
    else
        fprintf("input variables eror")
    end
end