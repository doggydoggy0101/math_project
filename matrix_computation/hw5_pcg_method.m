clc;clear;
addpath(genpath('utils')); verbose = true;

E = load('data/facebook.txt');
A = getLaplacian(E, verbose);

rng(42);

tol=1e-10; 
maxit=1e+5;

sigma = -0.01;
n = size(A, 1);

A_shift = A - sigma*speye(n);
b = randn(n,1);

fprintf("CG method:\n")
tic;
[sol,~,~,iter] = pcg_method(A_shift, b, tol, maxit);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);


prec_M = sparse(1:n, 1:n, diag(A_shift));

fprintf("CG method with preconditioning:\n")
tic;
[sol,~,~,iter] = pcg_method(A_shift, b, tol, maxit, prec_M);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);


prec_M1 = sparse(1:n, 1:n, diag(A_shift).^(0.5));
prec_M2 = prec_M1;

fprintf("CG method with left and right preconditioning:\n")
tic;
[sol,~,~,iter] = pcg_method(A_shift, b, tol, maxit, prec_M1, prec_M2);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);


lower_L = tril(A_shift, -1);
diag_D = sparse(1:n,1:n,diag(A_shift));
w = 1.15;
D_omegaL = diag_D + w*lower_L;

fprintf("CG method with SSOR preconditioning:\n")
tic;
[sol,~,~,iter] = pcg(A_shift, b, tol, maxit, @(x)prec_SSOR(x, D_omegaL, diag_D));
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);


function sol = prec_SSOR(rhs, D_omegaL, diag_D)
    sol = D_omegaL' \ (diag_D * (D_omegaL \ rhs));
end