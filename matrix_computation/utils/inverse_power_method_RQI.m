function [eigval, eigvec, sigma] = inverse_power_method_RQI(matrix, epsilon, iter_max, sigma, verbose)

    eps = epsilon;
    err = Inf;
    iter = 0;
    
    n = size(matrix,1);
    matrix_shift = matrix - sigma*speye(n);

    u = matrix_shift\randn(n,1); % initial guess
    u = u / norm(u); % normalize initial guess
    lambda = 1; 
    lambda_k = sigma;
    
    if verbose
        tic
    end

    while (err > eps && iter < iter_max)
        matrix_ = matrix - lambda_k*speye(n);
        v = matrix_\u;
        mu = norm(v);
        u = v/mu;
        lambda_k = dot(matrix*u,u);
        err = abs(lambda-lambda_k); % criterion
        lambda = lambda_k;
        iter = iter + 1;
    end

    if verbose
        toc
        fprintf("iterations: %.0f \n", iter);
    end
    
    eigval = lambda;
    eigvec = u;

    if verbose
        fprintf("eigenvalue closest to %.2f: %f \n",sigma, eigval);
    end
end