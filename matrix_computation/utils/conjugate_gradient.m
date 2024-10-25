function x = conjugate_gradient(b, A, tol, maxit, verbose)

    if verbose
        tic
    end

    n = size(A,1);
    x = randn(n,1); % initial guess

    r = b - A*x;
    v = r;
    rr_old = dot(r,r);

    for i = 1:maxit
        Av = A*v;

        alpha = rr_old/dot(v,Av);
        x = x + alpha*v;
        r = r - alpha*Av;

        rr_new = dot(r,r);

        if sqrt(rr_new) < tol
            break
        end

        beta = rr_new/rr_old;
        v = r + beta*v;

        rr_old = rr_new;
    end
    if verbose
        toc
        fprintf("iterations: %.0f\n", i)
    end
end