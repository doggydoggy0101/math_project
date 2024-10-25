clc;clear; 
addpath(genpath('utils')); verbose = true;

E = load('data/facebook.txt');
A = getLaplacian(E, verbose);

eps = 1e-7;
iter = 1e+3;
sigma = 0.01;

% Shifted Inverse Iteration
fprintf("SII:\n")
[eigval, eigvec] = inverse_power_method_SII(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n\n", check);


% Shifted Inverse Iteration with LU
fprintf("SII with LU:\n")
[eigval, eigvec] = inverse_power_method_LU(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n\n", check);


% Newton's Inverse Iteration
fprintf("NII:\n")
[eigval, eigvec, ~] = inverse_power_method_NII(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n\n", check);


% Rayleigh Quotient Iteration
fprintf("RQI:\n")
[eigval, eigvec, ~] = inverse_power_method_RQI(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n\n", check);