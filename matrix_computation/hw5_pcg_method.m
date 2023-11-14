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
[sol,~,~,iter] = pcg_method(b, A_shift, tol, maxit);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);


prec_M = sparse(1:n, 1:n, diag(A_shift));

fprintf("CG method with preconditioning:\n")
tic;
[sol,~,~,iter] = pcg_method(b, A_shift, tol, maxit, prec_M);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);


prec_M1 = sparse(1:n, 1:n, diag(A_shift).^(0.5));
prec_M2 = prec_M1;

fprintf("CG method with left and right preconditioning:\n")
tic;
[sol,~,~,iter] = pcg_method(b, A_shift, tol, maxit, prec_M1, prec_M2);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);