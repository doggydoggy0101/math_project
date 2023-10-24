function [U, H, k_i] = arnoldi_method(matrix, k, verbose)
    
    if verbose
        tic
    end

    n = size(matrix,1);

    u = matrix\randn(n,1); % initial guess
    u = u / norm(u); % normalize initial guess

    H = zeros(k+1, k);
    U = u;

    k_i = 0;
    for i = 1:k
        v = matrix*U(:,i);
    
        for j = 1:i
            H(j,i)  = U(:,j)' * v;
            v = v - H(j,i)*U(:,j);
        end
    
        H(i+1,i) = norm(v);
    
        if H(i+1,i) < 1e-16
            break
        end

        U(:, i+1) = v/H(i+1,i);
        k_i = k_i + 1;
    end

    U = U(:,1:k_i);
    H = H(1:k_i,:);

    if verbose
        toc
    end
end