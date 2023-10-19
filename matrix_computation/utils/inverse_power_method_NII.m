function [eigval, eigvec, sigma] = inverse_power_method_NII(matrix, epsilon, iter_max, sigma, verbose)

    eps = epsilon;
    err = Inf;
    iter = 0;
    
    n = size(matrix,1);
    matrix_shift = matrix - sigma*speye(n);

    u = matrix_shift\randn(n,1); % initial guess
    u = u / norm(u); % normalize initial guess

    [~,idx]  = max(abs(u)); % max eigenvalue index
    lambda_k = sigma;
    
    if verbose
        tic
    end

    while (err > eps && iter < iter_max)
        matrix_shift = matrix - lambda_k*speye(n);
        v = matrix_shift\u;
        mu = v(idx);
        u = v/mu;
        err = abs(1/mu); % criterion
        lambda_k = lambda_k + 1/mu;
        iter = iter + 1;
    end

    if verbose
        toc
        fprintf("iterations: %.0f \n", iter);
    end
    
    eigval = lambda_k;
    eigvec = u;

    if verbose
        fprintf("eigenvalue closest to %.2f: %f \n",sigma, eigval);
    end
end