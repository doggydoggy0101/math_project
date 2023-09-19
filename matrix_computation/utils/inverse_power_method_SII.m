function [eigval, eigvec] = inverse_power_method_SII(matrix, epsilon, iter_max, sigma, verbose)

    eps = epsilon;
    err = Inf;
    iter = 0;
    
    n = size(matrix, 1);
    u = [1,zeros(1,n-1)].'; % n x 1 column vector
    lambda1 = norm(u,2); % where the 2-norm is 1
    matrix = matrix - sigma*speye(n);
    
    if verbose
        tic
    end

    while (err > eps && iter < iter_max)
        v = matrix\u;
        lambda2 = norm(v,2);
        u = v/lambda2;

        err = abs(lambda1-lambda2); % criterion
        lambda1 = lambda2;
        iter = iter + 1;
    end

    if verbose
        toc
    end
    
    eigval = lambda1^-1 + sigma;
    eigvec = u;

    if verbose
        fprintf("eigenvalue closest to %.0f: %f \n",sigma, eigval);
    end
end

