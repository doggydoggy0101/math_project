clc;clear; 
addpath(genpath('utils')); verbose = false;

E = load('data/gowalla.txt'); 
A = getLaplacian(E, verbose);

k = 10;
k_max = 1e+5;
eps = 1e-7;

eigval_A=eigs(A, k);

for iterations = 10:10:50

    [~, H] = arnoldi_method(A, k, iterations, eps, verbose); eigval_H=eigs(H, k);
    [~, T] = lanczos_method(A, k, iterations, eps, verbose); eigval_T=eigs(T, k);

    subplot(5,1,iterations/10); ax = gca; ax.XAxisLocation='origin'; ax.YAxis.Visible='off'; hold on
    plot(eigval_H, zeros(k,1), 'o', MarkerSize=10, Color="#0072BD"); 
    plot(eigval_T, zeros(k,1), '^', MarkerSize=7, Color="red"); 
    plot(eigval_A, zeros(k,1), '.', MarkerSize=10, Color="black"); 
    title("Iteration: "+iterations); 
    axis([-300 15000 -1 1]);

    if iterations == 10
        lgnd = legend({'Arnoldi', 'Lanczos', 'Ground truth'},'Position', [0.78 0.88 0.1 0.1]);
    end
    fprintf("Plot iteration %.0f done.\n", iterations)
end