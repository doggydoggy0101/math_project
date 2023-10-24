clc;clear; 
addpath(genpath('utils'));

E = load('data/facebook.txt'); 
A = getLaplacian(E, true);
verbose = true;

k = 30;

% Arnoldi method
fprintf("Arnoldi:\n")
[U, H] = arnoldi_method(A, k, verbose);
[eigvec, eigval_H]= eigs(H, k);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval_H);
fprintf("norm(Ax-λx): %f \n\n", check);

% Lanczos method
fprintf("Lanczos:\n")
[U, T] = lanczos_method(A, k, verbose);
[eigvec, eigval_T]= eigs(T, k);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval_T);
fprintf("norm(Ax-λx): %f \n\n", check);


figure; ax = gca; ax.XAxisLocation='origin'; ax.YAxis.Visible='off'; hold on
plot(diag(eigval_H), 0, 'o', MarkerSize=10, Color="#0072BD"); % blue circles: eigvals of H
plot(diag(eigval_T), 0, '+', MarkerSize=10, Color="red"); % red crosses: eigvals of T