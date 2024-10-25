clc;clear;
addpath(genpath('utils')); verbose = true;

E = load('data/Pennsylvania.txt');
A = getLaplacian(E, verbose);

rng(42);

tol=1e-10; 
maxit=1e+5;

sigma = -0.01;
n = size(A, 1);

A_shift = A - sigma*speye(n);
b = randn(n,1);

% fprintf("steepest descent method:\n")
% sol = steepest_gradient(b, A_shift, tol, maxit, verbose);
% check = norm(A_shift*sol-b,2);
% fprintf("norm(Ax-b): %f \n\n", check);


fprintf("conjugate gradient method:\n")
sol = conjugate_gradient(b, A_shift, tol, maxit, verbose);
check = norm(A_shift*sol-b,2);
fprintf("norm(Ax-b): %f \n\n", check);


M = sparse(1:n, 1:n, diag(A_shift));

fprintf("preconditioned conjugate gradient method:\n")
sol = precondition_conjugate_gradient(b, A_shift, M, tol, maxit, verbose);
check = norm(A_shift*sol-b,2);
fprintf("norm(Ax-b): %f \n\n", check);