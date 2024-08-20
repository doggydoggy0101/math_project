clc;clear; 
addpath(genpath('utils')); verbose = true;

E = load('data/facebook.txt');
A = getLaplacian(E, verbose);

k = 10;
k_max = 1e+5;
eps = 1e-7;


% Arnoldi method
fprintf("Arnoldi:\n")
[U, H] = arnoldi_method(A, k, k_max, eps, verbose);
[eigvec, eigval]= eigs(H, k);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval);
fprintf("norm(Ax-λx): %f \n\n", check);

% Lanczos method
fprintf("Lanczos:\n")
[U, T] = lanczos_method(A, k, k_max, eps, verbose);
[eigvec, eigval]= eigs(T, k);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval);
fprintf("norm(Ax-λx): %f \n\n", check);


% plot
eigval_A=eigs(A, k); eigval_H=eigs(H, k); eigval_T=eigs(T, k);
figure; ax = gca; ax.XAxisLocation='origin'; ax.YAxis.Visible='off'; hold on
plot(eigval_H, zeros(k,1), 'o', MarkerSize=10, Color="#0072BD"); % blue circles: eigvals of H
plot(eigval_T, zeros(k,1), '^', MarkerSize=7, Color="red"); % red triangles: eigvals of T
plot(eigval_A, zeros(k,1), '.', MarkerSize=10, Color="black"); % black dots: eigvals of A
title("Largest "+k+" eigenvalues"); legend('Arnoldi', 'Lanczos', 'Ground truth')