import numpy as np
from utils.LieTheory import se2_vec_to_mat, se2_mat_to_vec

def compute_error(graph):

    err = 0
    for edge in graph.edges:
        # compute idx for nodes using lookup table
        i = graph.lut[edge.fromNode]
        j = graph.lut[edge.toNode]

        if edge.Type == 'P': 
            pose_i = se2_vec_to_mat(graph.x[i:i+3]) # stored as (x, y, theta)
            pose_j = se2_vec_to_mat(graph.x[j:j+3]) # stored as (x, y, theta)
       
            relpose = np.linalg.inv(pose_i)@pose_j # relative pose 
            gtruth = se2_vec_to_mat(edge.measurement) # ground truth, stored as (x, y, theta)
            err += np.linalg.norm(se2_mat_to_vec(np.linalg.inv(gtruth)@relpose))

        elif edge.Type == 'L': 
            pose = se2_vec_to_mat(graph.x[i:i+3]) # stored as (x, y, theta)
            landmark = graph.x[j:j+2]

            relmeas = np.linalg.inv(pose)[:2, :2]@np.expand_dims(landmark, axis=1) # relative measurement
            gtruth = np.expand_dims(edge.measurement, axis=1) # ground truth, homogeneous coordinate
            err += np.linalg.norm(relmeas - gtruth)

    return err