import numpy as np

from utils.dataloader import read_graph_g2o
from utils.visualize import plot_graph
from utils.error import compute_error
from utils.least_squares import GaussNewton


def pose_graph_optimization(graph, max_iteration=1000, tolerance=1e-4, gradType="Euclidean"):

    norm_prev = 1e+10
    for i in range(max_iteration):

        # compute increment
        dX = GaussNewton(graph, gradType=gradType)
        norm_dX = np.linalg.norm(dX)
        graph.x += dX
        err = compute_error(graph)
        print("iter {} error: {}".format(i+1, err))
            
        # stopping criteria
        if i >= 1 and np.abs(norm_dX - norm_prev) < tolerance:
            print("|dX| < threshold {}".format(tolerance))
            break

        norm_prev = norm_dX

    return graph



dataset = "intel" # pose constraint only (tol=0.01, 32 iters)
# dataset = "dlr" # pose constraint & landmark constraint (tol=0.1, iter=25)

graph = read_graph_g2o("data/" + dataset + ".g2o")
plot_graph(graph, dataset + "_init")

graph = pose_graph_optimization(graph, max_iteration=100, tolerance=0.01)
plot_graph(graph, dataset + "_optimized", constraint=False)