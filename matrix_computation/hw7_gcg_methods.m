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

prec_M = sparse(1:n, 1:n, diag(A_shift));

lower_L = tril(A_shift, -1);
diag_D = sparse(1:n,1:n,diag(A_shift));
w = 1.15;
D_omegaL = diag_D + w*lower_L;

% cg
fprintf("CG method:\n")
tic;
[sol,~,~,iter] = pcg_method(A_shift, b, tol, maxit);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);

fprintf("CG method with preconditioning:\n")
tic;
[sol,~,~,iter] = pcg_method(A_shift, b, tol, maxit, prec_M);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);

% gmres
fprintf("GMRES method:\n")
tic;
[sol,~,~,iter] = gmres_method(A_shift, b, tol, maxit);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);

fprintf("GMRES method with preconditioning:\n")
tic;
[sol,~,~,iter] = gmres_method(A_shift, b, tol, maxit, prec_M);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);

% bicg
fprintf("BiCG method:\n")
tic;
[sol,~,~,iter] = bicg_method(A_shift, b, tol, maxit);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);

fprintf("BiCG method with preconditioning:\n")
tic;
[sol,~,~,iter] = bicg_method(A_shift, b, tol, maxit, prec_M);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);

% cgs
fprintf("CGS method:\n")
tic;
[sol,~,~,iter] = cgs_method(A_shift, b, 1e-8, maxit);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);

fprintf("CGS method with preconditioning:\n")
tic;
[sol,~,~,iter] = cgs_method(A_shift, b, tol, maxit, prec_M);
toc;
check = norm(A_shift*sol-b,2);
fprintf("iterations: %.0f\n", iter)
fprintf("norm(Ax-b): %f \n\n", check);