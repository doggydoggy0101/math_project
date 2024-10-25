clc;clear; 
addpath(genpath('utils')); verbose = true;

E = load('data/gowalla.txt'); 
A = getLaplacian(E, verbose);

eps = 1e-7;
iter = 1e+5;

[eigval, eigvec] = power_method(A, eps, iter, verbose);

check = norm(A*eigvec - eigval*eigvec,2);
fprintf("norm(Ax-λx): %f \n", check);