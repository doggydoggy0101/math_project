clc;clear; 
addpath(genpath('utils'));

E = load('data/zachary.txt');
A = getLaplacian(E);

eps = 1e-3;
err = Inf;

n = size(A, 1);
u = [1,zeros(1,n-1)].'; % n x 1 column vector
lambda1 = norm(u,2); % where the 2-norm is 1

while err > eps
    v = A*u;
    lambda2 = norm(v,2);
    u = v/lambda2;
    err = abs(lambda1-lambda2);
    lambda1 = lambda2;
end

eigval = lambda1;
eigvec = u;

fprintf("largest eigenvalues: %f \n", eigval);
