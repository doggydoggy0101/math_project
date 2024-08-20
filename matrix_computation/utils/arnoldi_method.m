function [U, H] = arnoldi_method(matrix, k_wanted, k_max, tol, verbose)
    
    if verbose
        tic
    end

    n = size(matrix,1);

    u = matrix\randn(n,1); % initial guess
    u = u / norm(u); % normalize initial guess

    H = zeros(k_max+1, k_max);
    U = u;

    k_i = 0;
    for i = 1:k_max
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

        % criteria
        if k_i > 1
            [eigvec, eigval] = eigs(H(1:k_i,1:k_i), k_wanted);

            % define stopping criteria:
            % ritzvec = U(:,1:k_i)*eigvec;
            % loss = norm(matrix*ritzvec - ritzvec*eigval);

            % which is equivalent to:
            loss = abs(H(k_i+1,k_i))*norm(eigvec(k_i,:));

            if loss < tol
                break
            end
        end
        k_i = k_i + 1;
    end

    U = U(:, 1:k_i);
    H = H(1:k_i, 1:k_i);

    if verbose
        toc
        fprintf("iterations: %.0f \n", k_i);
        if k_wanted == 1
            fprintf("largest eigenvalue: %f\n", eigval);
        else
            fprintf("largest %.0f eigenvalues:\n\n", k_wanted);
            disp(diag(eigval))
        end
    end
end