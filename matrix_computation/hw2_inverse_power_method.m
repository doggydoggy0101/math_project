clc;clear; 
addpath(genpath('utils'));

E = load('data/zachary.txt'); 
A = getLaplacian(E);

eps = 1e-5;
iter = 1e+2;
sigma = 18;
verbose = true;

% Shifted Inverse Iteration
fprintf("SII:\n")
[eigval, eigvec] = inverse_power_method_SII(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n", check);

% Newton's Inverse Iteration
fprintf("NII:\n")
[eigval, eigvec, sigma] = inverse_power_method_RQI(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n", check);

% Rayleigh Quotient Iteration
fprintf("RQI:\n")
[eigval, eigvec, sigma] = inverse_power_method_RQI(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n", check);
