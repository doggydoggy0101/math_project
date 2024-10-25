function x = steepest_gradient(b, A, tol, maxit, verbose)

    if verbose
        tic
    end

    n = size(A,1);
    x = randn(n,1); % initial guess

    for i = 1:maxit
        r = b - A*x;

        rr = dot(r,r);

        if sqrt(rr) < tol
            break
        end

        alpha = rr/dot(r,A*r);
        x = x + alpha*r;
    end

    if verbose
        toc
        fprintf("iterations: %.0f\n", i)
    end
end