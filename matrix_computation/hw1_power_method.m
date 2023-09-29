clc;clear; 
addpath(genpath('utils'));

E = load('data/facebook.txt'); 
A = getLaplacian(E, true);

eps = 1e-8;
iter = 1e+5;
verbose = true;

[eigval, eigvec] = power_method(A, eps, iter, verbose);

check = norm(A*eigvec - eigval*eigvec,2);
fprintf("norm(Ax-λx): %f \n", check);


% addpath(genpath('sample_code'));
% fprintf("---------------------------------\nSample code\n");
% tic;
% [eigval, eigvec, ~] = PowerMethod_Norm(A, iter, eps);
% toc;
% check = norm(A*eigvec - eigval*eigvec,2);
% fprintf("largest eigenvalue: %f \n", eigval)
% fprintf("norm(Ax-λx): %f \n", check);