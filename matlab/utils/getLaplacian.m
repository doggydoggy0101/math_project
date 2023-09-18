function mtx_L = getLaplacian(E)

    n = max(max(E));
    m = size(E,2);
    
    if (m == 2 )
        mtx_L  = sparse(E(:,1), E(:,2), 1, n, n); 
    else
        mtx_L = sparse(E(:,1), E(:,2), E(:,3), n, n);
    end
    
    
    D_L = diag(mtx_L);
    
    if ( ~isempty(find(D_L ~= 0, 1)) )
        mtx_L = mtx_L - sparse(1:n, 1:n, D_L);
    end        
    
    mtx_L = mtx_L + mtx_L';
    mtx_L = diag(sum(mtx_L, 2)) - mtx_L; % Laplacian matrix

end

