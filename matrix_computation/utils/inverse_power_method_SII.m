function [eigval, eigvec] = inverse_power_method_SII(matrix, epsilon, iter_max, sigma, verbose)

    eps = epsilon;
    err = Inf;
    iter = 0;

    n = size(matrix,1);
    matrix_shift = matrix - sigma*speye(n);

    u = matrix_shift\randn(n,1); % initial guess
    u = u / norm(u); % normalize initial guess

    [~,idx]  = max(abs(u)); % max eigenvalue index
    lambda1=1;
    
    if verbose
        tic
    end

    while (err > eps && iter < iter_max)
        v = matrix_shift\u;
        mu_ = v(idx);
        u = v/mu_;
        err = abs(lambda1-sigma-1/mu_); % criterion
        lambda1 = sigma + 1/mu_;
        iter = iter + 1;
    end

    if verbose
        toc
        fprintf("iterations: %.0f \n", iter);
    end
    
    eigval = lambda1;
    eigvec = u;

    if verbose
        fprintf("eigenvalue closest to %.2f: %f \n",sigma, eigval);
    end
end

