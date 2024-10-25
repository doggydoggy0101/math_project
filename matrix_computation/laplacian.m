clc;clear; 
addpath(genpath('utils'));

E = load('data/graph.txt'); 
mtx_L = getLaplacian(E, true);

% plotGraph(E)

disp(full(mtx_L))