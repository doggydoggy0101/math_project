import numpy as np
import matplotlib.pyplot as plt

def get_poses_landmarks(graph):
    poses = []
    landmarks = []

    for nodeId in graph.nodes:
        dimension = len(graph.nodes[nodeId])
        offset = graph.lut[nodeId]

        if dimension == 3:
            pose = graph.x[offset:offset + 3]
            poses.append(pose)
        elif dimension == 2:
            landmark = graph.x[offset:offset + 2]
            landmarks.append(landmark)

    return poses, landmarks


def plot_graph(graph, figname, constraint=True):
    # initialize figure
    plt.figure(1, figsize=(10,6))
    plt.clf()

    # get a list of all poses and landmarks
    poses, landmarks = get_poses_landmarks(graph)

    # plot robot poses
    if len(poses) > 0:
        poses = np.stack(poses, axis=0)
        plt.plot(poses[:, 0], poses[:, 1], 'o', color="#4863A0")

    # plot landmarks
    if len(landmarks) > 0:
        landmarks = np.stack(landmarks, axis=0)
        plt.plot(landmarks[:, 0], landmarks[:, 1], '^', color="#F75D59")

    # plot edges/constraints
    if constraint:
        poseEdgesP1 = []
        poseEdgesP2 = []
        landmarkEdgesP1 = []
        landmarkEdgesP2 = []
        
        for edge in graph.edges:
            fromIdx = graph.lut[edge.fromNode]
            toIdx = graph.lut[edge.toNode]
            if edge.Type == 'P':
                poseEdgesP1.append(graph.x[fromIdx:fromIdx + 3])
                poseEdgesP2.append(graph.x[toIdx:toIdx + 3])
            elif edge.Type == 'L':
                landmarkEdgesP1.append(graph.x[fromIdx:fromIdx + 2])
                landmarkEdgesP2.append(graph.x[toIdx:toIdx + 2])

        poseEdgesP1 = np.stack(poseEdgesP1, axis=0)
        poseEdgesP2 = np.stack(poseEdgesP2, axis=0)
        plt.plot(np.concatenate((poseEdgesP1[:, 0], poseEdgesP2[:, 0])),
                np.concatenate((poseEdgesP1[:, 1], poseEdgesP2[:, 1])), color="#808080", linewidth=0.5)

    plt.savefig("docs/" + figname + ".png")

    return