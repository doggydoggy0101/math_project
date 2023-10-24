function [U, T] = lanczos_method(matrix, k, verbose)

    if verbose
        tic
    end

    n = size(matrix,1);

    u = matrix\randn(n,1); % initial guess
    u = u / norm(u); % normalize initial guess

    H = zeros(k+1, k);
    U = u;

    v = matrix * U(:,1);
    T(1,1) = v' * U(:,1); % alpha

    v = v - T(1,1) * U(:,1);
    T(2,1) = norm(v); % beta

    U(:,2) = v / T(2,1);

    for i = 2:k

        v = matrix * U(:,i);
        T(i-1,i) = T(i,i-1); 

        v = v - T(i-1,i) * U(:,i-1); 
        T(i,i) = v' * U(:,i); % alpha

        v = v - T(i,i) * U(:,i); 
        T(i+1, i) = norm(v); % beta

        U(:,i+1) = v / T(i+1, i);
    end
    
    U = U(:,1:k);
    T = T(1:k,:);

    if verbose
        toc
    end
end