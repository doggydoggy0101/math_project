clc;clear; 
addpath(genpath('utils'));

E = load('data/facebook.txt'); 
A = getLaplacian(E, true);
verbose = true;

k = 30;
eps = 1e-7;

% Arnoldi method
fprintf("Arnoldi:\n")
[U, H] = arnoldi_method(A, k, eps, verbose);
[eigvec, eigval]= eigs(H, 1);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval(1));
fprintf("norm(Ax-λx): %f \n\n", check);

% Lanczos method
fprintf("Lanczos:\n")
[U, T] = lanczos_method(A, k, eps, verbose);
[eigvec, eigval]= eigs(T, 1);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval(1));
fprintf("norm(Ax-λx): %f \n\n", check);

% plot
eigval_A=eigs(A, 10); eigval_H=eigs(H, 10); eigval_T=eigs(T, 10);
figure; ax = gca; ax.XAxisLocation='origin'; ax.YAxis.Visible='off'; hold on
plot(eigval_H, zeros(10,1), 'o', MarkerSize=10, Color="#0072BD"); % blue circles: eigvals of H
plot(eigval_T, zeros(10,1), '^', MarkerSize=7, Color="red"); % red crosses: eigvals of T
plot(eigval_A, zeros(10,1), '.', MarkerSize=10, Color="black"); % red crosses: eigvals of T
title('Largest 10 eigenvalues'); legend('Arnoldi', 'Lanczos', 'Ground truth')