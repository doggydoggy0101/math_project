clc;clear; 
addpath(genpath('utils'));

E = load('data/loc-brightkite_edges.txt');
A = getLaplacian(E);

eps = 1e-5;
err = Inf;
verbose = true;

[eigval, eigvec] = power_method(A, eps, verbose);