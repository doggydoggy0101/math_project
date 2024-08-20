clc;clear; 
addpath(genpath('utils')); verbose = true;

E = load('data/facebook.txt');
A = getLaplacian(E, verbose);

sigma = 0.01;
n = size(A,1);
M1 = A - sigma*speye(n);

x = randn(n,1);

fprintf("\nLU factorization for matrix:\n")
tic
[M1_L, M1_U, M1_Perm_LU] = lu(M1);
toc
fprintf("Solve linear system for matrix:\n")
tic
b1 = M1_U \ (M1_L \ (M1_Perm_LU*x));
toc

fprintf("\nLU factorization for permutated matrix:\n")
tic
Perm_amd_vec = amd(M1);
M2 = M1(Perm_amd_vec, Perm_amd_vec);
M2_Perm_amd = sparse(Perm_amd_vec, 1:n, ones(n,1));
[M2_L, M2_U, M2_Perm_LU] = lu(M2);
toc
fprintf("Solve linear system for permutated matrix:\n")
tic
b2 = M2_Perm_amd*(M2_U \ (M2_L \ (M2_Perm_LU*x(Perm_amd_vec,:))));
toc

fprintf("\ncheck 2 solutions norm(b1-b2): %f \n\n", norm(b1-b2));

figure;
subplot(1,2,1); spy(M1_U); title('Before permutation');
subplot(1,2,2); spy(M2_U); title('After permutation');