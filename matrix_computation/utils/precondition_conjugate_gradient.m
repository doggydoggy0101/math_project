function x = precondition_conjugate_gradient(b, A, M, tol, maxit, verbose)

    if verbose
        tic
    end

    n = size(A,1);
    x = randn(n,1); % initial guess

    r = b - A*x;
    z = M\r;
    v = z;
    rr_old = dot(r,z);

    for i = 1:maxit
        Av = A*v;

        alpha = rr_old/dot(v,Av);
        x = x + alpha*v;
        r = r - alpha*Av;
        
        z = M\r;
        rr_new = dot(r,z);

        if sqrt(rr_new) < tol
            break
        end

        beta = rr_new/rr_old;
        v = z + beta*v;

        rr_old = rr_new;
    end
    if verbose
        toc
        fprintf("iterations: %.0f\n", i)
    end
end