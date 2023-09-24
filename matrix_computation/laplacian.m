clc;clear; 
addpath(genpath('utils'));

E = load('data/brightkite.txt'); 
mtx_L = getLaplacian(E, true);

% plotGraph(E)