function [eigval, eigvec] = power_method(matrix, epsilon, verbose)

    eps = epsilon;
    err = Inf;

    n = size(matrix, 1);
    u = [1,zeros(1,n-1)].'; % n x 1 column vector
    lambda1 = norm(u,2); % where the 2-norm is 1
    
    if verbose
        tic
    end

    while err > eps
        v = matrix*u;
        lambda2 = norm(v,2);
        u = v/lambda2;
        err = abs(lambda1-lambda2); % criterion
        lambda1 = lambda2;
    end

    if verbose
        toc
    end
    
    eigval = lambda1;
    eigvec = u;

    if verbose
        fprintf("largest eigenvalues: %f \n", eigval);
    end

end

