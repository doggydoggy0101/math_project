function [eigval, eigvec] = power_method(matrix, epsilon, iter_max, verbose)

    eps = epsilon;
    err = Inf;
    iter = 0;

    n = size(matrix, 1);
    u = randn(n,1); % initial guess
    u = u / norm(u); % normalize initial guess
    lambda = 1; % where the 2-norm is 1
    
    if verbose
        tic
    end

    while (err > eps && iter < iter_max)
        v = matrix*u;
        lambda_ = norm(v); % v(1)
        u = v/lambda_;
        % criterion
        err = abs(lambda-lambda_); 
        % err = norm(matrix*u - u*lambda_,2);

        lambda = lambda_;
        iter = iter + 1;
    end

    eigval = lambda;
    eigvec = u;

    if verbose
        toc
        fprintf("iterations: %.0f \n", iter);
        fprintf("largest eigenvalue: %f \n", eigval);
    end

end

