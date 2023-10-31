function [U, T] = lanczos_method(matrix, k, tol, verbose)

    if verbose
        tic
    end

    n = size(matrix,1);

    u = matrix\randn(n,1); % initial guess
    U = u / norm(u); % normalize initial guess

    v = matrix * U(:,1);
    T(1,1) = v' * U(:,1); % alpha

    v = v - T(1,1) * U(:,1);
    T(2,1) = norm(v); % beta

    U(:,2) = v / T(2,1);

    for i = 2:k

        T(i-1,i) = T(i,i-1); 

        v = matrix * U(:,i);
        T(i,i) = v' * U(:,i); % alpha

        v = v - T(i,i) * U(:,i) - T(i-1,i) * U(:,i-1); 
        T(i+1, i) = norm(v); % beta

        U(:,i+1) = v / T(i+1, i);

        % criteria
        [eigvec, eigval] = eigs(T(1:i, 1:i), 1);

        % define stopping criteria:
        % ritzvec = U(:,1:i)*eigvec;
        % loss1 = norm(matrix*ritzvec - ritzvec*eigval);

        % which is equivalent to:
        loss = abs(T(i+1, i))*abs(eigvec(i));

        if loss < tol
            break
        end

    end
    U = U(:, 1:i);
    T = T(1:i, 1:i);

    if verbose
        toc
        fprintf("iterations: %.0f \n", i);
        fprintf("largest eigenvalue: %f \n", eigval);
    end
end