# Implementation of 
# [1] Grisetti, G., Kümmerle, R., Stachniss, C., & Burgard, W. (2010). 
#     A tutorial on graph-based SLAM. 
#     IEEE Intelligent Transportation Systems Magazine, 2(4), 31-43.
# [2] Sola, J., Deray, J., & Atchuthan, D. (2018). 
#     A micro Lie theory for state estimation in robotics. 
#     arXiv preprint arXiv:1812.01537.

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

from utils.LieTheory import se2_vec_to_mat, se2_Log, se2_Jacobian_right, se2_Jacobian_inversion
### TODO Jacobian by Lie theory is not working

def compute_Jacobian_and_residual(node1, node2, gtruth, edgeType, gradType):
    ''' [1] Grisetti, G., Kümmerle, R., Stachniss, C., & Burgard, W. (2010). 
            A tutorial on graph-based SLAM. 
            IEEE Intelligent Transportation Systems Magazine, 2(4), 31-43.
        [2] Sola, J., Deray, J., & Atchuthan, D. (2018). 
            A micro Lie theory for state estimation in robotics. 
            arXiv preprint arXiv:1812.01537. '''
    if edgeType == "P":

        pose_i = node1
        pose_j = node2

        if gradType == "Euclidean":
            # x,y
            t_i = pose_i[:2]
            t_j = pose_j[:2]
            t_ij = gtruth[:2]
            # theta
            theta_i = pose_i[2]
            theta_j = pose_j[2]
            theta_ij = gtruth[2]

            rot_i = se2_vec_to_mat(pose_i)[:2, :2]
            rot_ij = se2_vec_to_mat(gtruth)[:2, :2]

            # derivative of rot_i with respect to theta_i
            drot_i = np.array([[-np.sin(theta_i), -np.cos(theta_i)],
                               [np.cos(theta_i), -np.sin(theta_i)]])

            # residual 
            res = np.hstack((rot_ij.T@rot_i.T@(t_j - t_i) - rot_ij.T@t_ij, (theta_j - theta_i) - theta_ij))
            # Jacobian of residual with respect to pose_i (Equation (32) of [1])
            J_i = -np.eye(3)
            J_i[:2, :2] = -rot_ij.T@rot_i.T
            J_i[:2, 2] = rot_ij.T@drot_i.T@(t_j - t_i)
            # Jacobian of residual with respect to pose_j (Equation (32) of [2])
            J_j = np.eye(3)
            J_j[:2, :2] = rot_ij.T@rot_i.T
        
        if gradType == "Lie":
            ### TODO debug
            res = se2_Log(np.linalg.inv(se2_vec_to_mat(gtruth))@np.linalg.inv(se2_vec_to_mat(pose_i))@se2_vec_to_mat(pose_j))
            J_j = np.linalg.inv(se2_Jacobian_right(res))
            J_i = J_j@se2_Jacobian_inversion(np.linalg.inv(se2_vec_to_mat(pose_i))@se2_vec_to_mat(pose_j))

        return J_i, J_j, res

    if edgeType == "L":

        pose = node1
        landmark = node2

        if gradType == "Euclidean":
            # x,y
            t_i = pose[:2]
            t_j = landmark
            z_ij = gtruth
            # theta
            theta_i = pose[2]
            rot_i = se2_vec_to_mat(pose)[:2, :2]

            # derivative of rot_i with respect to theta_i
            drot_i = np.array([[-np.sin(theta_i), -np.cos(theta_i)],
                            [np.cos(theta_i), -np.sin(theta_i)]])
            # residual
            res = rot_i.T@(t_j - t_i) - z_ij
            # Jacobian of residual with respect to pose_i
            J_i = np.zeros((2, 3))
            J_i[:2, :2] = -rot_i.T
            J_i[:2, 2] = drot_i.T@(t_j - t_i)
            # Jacobian of residual with respect to landmark_j 
            J_j = rot_i.T
        
        if gradType == "Lie":
            ### TODO write pose & landmark constraint residual
            ### TODO derive Jacobians respectively
            pass
        
        return J_i, J_j, res


def GaussNewton(graph, gradType="Euclidean"):
    ''' [1] Grisetti, G., Kümmerle, R., Stachniss, C., & Burgard, W. (2010). 
            A tutorial on graph-based SLAM. 
            IEEE Intelligent Transportation Systems Magazine, 2(4), 31-43. '''
    H = np.zeros((len(graph.x), len(graph.x)))
    b = np.expand_dims(np.zeros(len(graph.x)), axis=1)

    needToAddPrior = True

    for edge in graph.edges:
        # compute idx for nodes using lookup table
        i = graph.lut[edge.fromNode]
        j = graph.lut[edge.toNode]

        if edge.Type == 'P':
            pose1 = graph.x[i:i+3]
            pose2 = graph.x[j:j+3]

            gtruth = edge.measurement
            mat_info = edge.information
            J_i, J_j, res = compute_Jacobian_and_residual(pose1, pose2, gtruth, edgeType=edge.Type, gradType=gradType)
 
            # update H (Equation (18) in [1])
            H[i:i+3, i:i+3] += J_i.T@mat_info@J_i
            H[i:i+3, j:j+3] += J_i.T@mat_info@J_j
            H[j:j+3, i:i+3] += J_j.T@mat_info@J_i
            H[j:j+3, j:j+3] += J_j.T@mat_info@J_j
            # update b (Equation (19) in [1])
            b[i:i+3] += (J_i.T@mat_info@res).reshape(3, 1)
            b[j:j+3] += (J_j.T@mat_info@res).reshape(3, 1)
            # add prior for one pose of this edge
            if needToAddPrior:
                H[i:i+3, i:i+3] = H[i:i+3, i:i+3] + 1000 * np.eye(3)
                needToAddPrior = False

        elif edge.Type == 'L':
            pose = graph.x[i:i+3]
            landmark = graph.x[j:j+2]

            gtruth = edge.measurement
            mat_info = edge.information
            J_i, J_j, res = compute_Jacobian_and_residual(pose, landmark, gtruth, edgeType=edge.Type, gradType=gradType)
            
            # update H (Equation (18) in [1])
            H[i:i+3, i:i+3] += J_i.T@mat_info@J_i
            H[i:i+3, j:j+2] += J_i.T@mat_info@J_j
            H[j:j+2, i:i+3] += J_j.T@mat_info@J_i
            H[j:j+2, j:j+2] += J_j.T@mat_info@J_j
            # update b (Equation (19) in [1])
            b[i:i+3] += (J_i.T@mat_info@res).reshape(3, 1)
            b[j:j+2] += (J_j.T@mat_info@res).reshape(2, 1)
       
    # solve sparse linear system
    H_sparse = csr_matrix(H)
    dx = spsolve(H_sparse, -b).squeeze()

    return dx
