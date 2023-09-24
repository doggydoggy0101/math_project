function [eigval, eigvec, sigma] = inverse_power_method_NII(matrix, epsilon, iter_max, sigma, verbose)

    eps = epsilon;
    err = Inf;
    iter = 0;
    
    n = size(matrix, 1);
    u = [1,zeros(1,n-1)].'; % n x 1 column vector
    lambda1 = sigma;
    
    if verbose
        tic
    end

    while (err > eps && iter < iter_max)
        matrix_ = matrix - lambda1*speye(n);
        v = matrix_\u;
        lambda2 = norm(v,2);
        u = v/lambda2;
        lambda1 = sigma + 1/lambda2;

        err = abs(lambda1-lambda2); % criterion
        iter = iter + 1;
    end

    if verbose
        toc
    end
    
    eigval = lambda1;
    eigvec = u;

    if verbose
        fprintf("eigenvalue closest to %.2f: %f \n",sigma, eigval);
    end
end