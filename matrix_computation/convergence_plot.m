clc;clear;
addpath(genpath('utils')); verbose = true;

k = 1:0.1:50;
x = 20;

plot(k, SD(x,k), LineWidth=1); hold on
plot(k, CG(x,k), LineWidth=1); hold off
xlabel("k"); legend({"Steepest Descent Method", "Conjugate Gradient Method"})

function rate = SD(kappa, k)
    rate = ((kappa-1)./(kappa+1)).^k;
end

function rate = CG(kappa, k)
    rate = 2*((sqrt(kappa)-1)./(sqrt(kappa)+1)).^k;
end