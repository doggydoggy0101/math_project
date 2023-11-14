clc;clear;
addpath(genpath('utils')); verbose=true;

E = load('data/facebook.txt');
A = getLaplacian(E, verbose);

m = 30;

eps = 1e-7;
iter = 1e+3;
sigma = -0.01;
n = size(A, 1);

A_shift = A - sigma*speye(n);

factor.Perm_amd_vec = amd(A_shift);
A_Perm = A_shift(factor.Perm_amd_vec, factor.Perm_amd_vec);
factor.Perm_amd = sparse(factor.Perm_amd_vec, 1:n, ones(n,1));
[factor.L, factor.U, factor.Perm_LU] = lu(A_Perm);

fprintf("Matlab eigen solver:\n")
[eigvec, eigval] = eigs(A, m, 'smallestabs', Tolerance=eps, MaxIterations=iter, SubspaceDimension=3*m);
check = norm(A*eigvec - eigvec*eigval,2);
fprintf("norm(Ax-λx): %f \n\n", check);

fprintf("Gaussian elimination:\n")
[eigvec, eigval] = eigs(@(x)GE_Shift_LS(x, A_shift),n, m, 'largestabs', Tolerance=eps, MaxIterations=iter, IsFunctionSymmetric=1);
eigval = diag(sigma + 1./diag(eigval));
check = norm(A*eigvec - eigvec*eigval,2);
fprintf("norm(Ax-λx): %f \n\n", check);

fprintf("LU factorization:\n")
[eigvec, eigval] = eigs(@(x)Shift_A_inv_b(x, factor), n, m, 'largestabs', Tolerance=eps, MaxIterations=iter, IsFunctionSymmetric=1);
eigval = diag(sigma + 1./diag(eigval));
check = norm(A*eigvec - eigvec*eigval,2);
fprintf("norm(Ax-λx): %f \n\n", check);

tol=1e-10; maxit=1e+5;

fprintf("Iterative method:\n")
[eigvec, eigval] = eigs(@(x)pcg_method(x, A_shift, tol, maxit), n, m, 'largestabs', Tolerance=eps, MaxIterations=iter, IsFunctionSymmetric=1);
eigval = diag(sigma + 1./diag(eigval));
check = norm(A*eigvec - eigvec*eigval,2);
fprintf("norm(Ax-λx): %f \n\n", check);


function sol = GE_Shift_LS(b, A)
    sol = A \ b;
end

function sol = Shift_A_inv_b(rhs, factor)
    sol = factor.Perm_amd * (factor.U \ (factor.L \ (factor.Perm_LU * rhs(factor.Perm_amd_vec,:))));
end