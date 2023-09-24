clc;clear; 
addpath(genpath('utils'));

E = load('data/facebook.txt');
A = getLaplacian(E, true);

% D = eig(full(A));
% disp(D)

eps = 1e-5;
iter = 1e+3;
sigma = 0.01;
verbose = true;

% Shifted Inverse Iteration
fprintf("SII:\n")
[eigval, eigvec] = inverse_power_method_SII(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n", check);

% Newton's Inverse Iteration
fprintf("NII:\n")
[eigval, eigvec, ~] = inverse_power_method_NII(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n", check);

% Rayleigh Quotient Iteration
fprintf("RQI:\n")
[eigval, eigvec, ~] = inverse_power_method_RQI(A, eps, iter, sigma, verbose);
check = norm(A*eigvec - eigval*eigvec, 2);
fprintf("norm(Ax-λx): %f \n", check);