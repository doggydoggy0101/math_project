import numpy as np
from sknetwork.ranking import PageRank
from sknetwork.visualization import visualize_graph

import scipy.io

mat = scipy.io.loadmat('data/gre_343.mat')

adjacency = mat['Problem'][0][0][1] # 1 & 2
pagerank = PageRank()
scores = pagerank.fit_predict(adjacency)
image = visualize_graph(adjacency, scores=np.log(scores), node_size=4, edge_width=1, width=1080, height=720)

# notebook
# from IPython.display import SVG 
# SVG(image)