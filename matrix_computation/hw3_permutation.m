clc;clear; 
addpath(genpath('utils'));

E = load('data/facebook.txt');
A = getLaplacian(E, true);

sigma = 0.01;
n = size(A,1);
U1 = A - sigma*speye(n);

x = randn(n,1);

fprintf("\nLU factorization for U_1:\n")
tic
[U1_Low_L, U1_upper_U, U1_Perm_LU] = lu(U1);
toc
fprintf("Solve linear system for U_1:\n")
tic
b1 = U1_upper_U \ (U1_Low_L \ (U1_Perm_LU * x));
toc

fprintf("\nLU factorization for U_2:\n")
tic
Perm_amd_vec = amd(U1);
U2 = U1(Perm_amd_vec, Perm_amd_vec);
U2_Perm_amd = sparse(Perm_amd_vec, 1:n, ones(n,1));
[U2_Low_L, U2_upper_U, U2_Perm_LU] = lu(U2);
toc
fprintf("Solve linear system for U_2:\n")
tic
b2 = U2_Perm_amd * (U2_upper_U \ (U2_Low_L \ (U2_Perm_LU * x(Perm_amd_vec,:))));
toc

fprintf("\ncheck 2 solutions norm(b1-b2): %f \n\n", norm(b1-b2));

figure;
subplot(1,2,1); spy(U1); title('Before permutation');
subplot(1,2,2); spy(U2); title('After permutation');