clc;clear; 
addpath(genpath('utils'));

E = load('data/gowalla.txt'); 
A = getLaplacian(E, true);
verbose = true;

k = 30;

% Arnoldi method
fprintf("Arnoldi:\n")
[U, H] = arnoldi_method(A, k, verbose);
[eigvec, eigval]= eigs(H);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval);
fprintf("norm(Ax-λx): %f \n\n", check);

% Lanczos method
fprintf("Lanczos:\n")
[U, T] = lanczos_method(A, k, verbose);
[eigvec, eigval]= eigs(T);
eigvec = U*eigvec;
check = norm(A*eigvec - eigvec*eigval);
fprintf("norm(Ax-λx): %f \n\n", check);

eigH = eig(H); eigT = eig(T); 
figure; ax = gca; ax.XAxisLocation='origin'; ax.YAxis.Visible='off'; hold on
plot(eigH, 0, 'o', MarkerSize=10, Color="#0072BD"); % blue circles: e.vals of H
plot(eigT, 0, '+', MarkerSize=10, Color="red"); % red crosses: e.vals of T