function plotGraph(E)

    G = graph(E(:,1), E(:,2));
    
    [bins,binsizes] = conncomp(G);
    idx_first_graph = binsizes(bins) == max(binsizes);
    
    SG = subgraph(G, idx_first_graph);
    plot(SG)

end