clc;clear; 
addpath(genpath('utils'));

E = load('data/zachary.txt');

mtx_L = getLaplacian(E);

plotGraph(E)