clc;clear;
addpath(genpath('utils')); verbose = false;

rng(42);

tol=1e-10; 
maxit=1e+5;

data_title = ["brightkite", "gowalla", "Pennsylvania"];
lower_bdd = 0.6;
upper_bdd = 1.6;
step = 0.1;

for idx = 1:1:3

    E = load('data/'+data_title(idx)+'.txt');
    A = getLaplacian(E, verbose);
    n = size(A, 1);
    b = randn(n,1);

    x = []; y = [];

    for i = lower_bdd:step:upper_bdd
        x = [x,i];
        y = [y, plot_SSOR(i, A, b, tol, maxit)];
    end

    [min_y, min_index] = min(y);

    subplot(3,1,idx); ax = gca; 
    plot(x, y, '--.', LineWidth=1, MarkerSize=12); hold on
    min_plot = plot(x(min_index), min_y, '.r', MarkerSize=12); hold off
    xlabel("w"); ylabel("iters"); xlim([lower_bdd upper_bdd])
    legend(min_plot, strcat('optimal w = ', num2str(x(min_index)))); title(data_title(idx))

    fprintf(strcat(num2str(data_title(idx)), ' done...\n'));
end

function sol = prec_SSOR(rhs, D_omegaL, diag_D)
    sol = D_omegaL' \ (diag_D * (D_omegaL \ rhs));
end

function y = plot_SSOR(w, A, b, tol, maxit)
    n = size(A, 1);
    sigma = -0.01;
    A_shift = A - sigma*speye(n);
    lower_L = tril(A_shift, -1);
    diag_D = sparse(1:n,1:n,diag(A_shift));
    D_omegaL = diag_D + w*lower_L;
    [~,~,~,y] = pcg(A_shift, b, tol, maxit, @(x)prec_SSOR(x, D_omegaL, diag_D));
end