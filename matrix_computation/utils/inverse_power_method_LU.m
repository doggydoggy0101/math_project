function [eigval, eigvec] = inverse_power_method_LU(matrix, epsilon, iter_max, sigma, verbose)

    eps = epsilon;
    err = Inf;
    iter = 0;

    n = size(matrix,1);
    matrix_shift = matrix - sigma*speye(n);

    u = randn(n,1);% initial guess

    if verbose
        tic
    end

    % [L,U,P] = lu(matrix_shift);
    % u = U\(L\(P*u)); 

    Perm_amd_vec = amd(matrix_shift);
    W_reorder = matrix_shift(Perm_amd_vec, Perm_amd_vec);
    Perm_amd_mtx = sparse(Perm_amd_vec, 1:n, ones(n,1));
    [mtx_L, mtx_U, mtx_Perm_LU] = lu(W_reorder);
    u = Perm_amd_mtx*(mtx_U \ (mtx_L \ (mtx_Perm_LU*u(Perm_amd_vec,:))));

    u = u / norm(u); % normalize initial guess
    [~,idx]  = max(abs(u)); % max eigenvalue index
    lambda1=1;

    if verbose
        timeLU = toc;
        fprintf("LU factorization time: %f seconds.\n", timeLU)
        tic
    end

    while (err > eps && iter < iter_max)
        v = Perm_amd_mtx*(mtx_U \ (mtx_L \ (mtx_Perm_LU*u(Perm_amd_vec,:))));
        mu_ = v(idx);
        u = v/mu_;
        err = abs(lambda1-sigma-1/mu_); % criterion
        lambda1 = sigma + 1/mu_;
        iter = iter + 1;
    end

    if verbose
        toc;
        fprintf("iterations: %.0f \n", iter);
    end
    
    eigval = lambda1;
    eigvec = u;

    if verbose
        fprintf("eigenvalue closest to %.2f: %f \n", sigma, eigval);
    end
end

