clc;clear; 
addpath(genpath('utils'));

E = load('data/brightkite.txt'); 
A = getLaplacian(E, true);

eps = 1e-7;
iter = 1e+5;
verbose = true;

[eigval, eigvec] = power_method(A, eps, iter, verbose);

check = norm(A*eigvec - eigval*eigvec,2);
fprintf("norm(Ax-λx): %f \n", check);