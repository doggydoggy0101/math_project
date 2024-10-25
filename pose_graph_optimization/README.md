# :robot: Pose graph optimization

Numercial examples of blog: [Pose graph optimization](https://dgbshien.com/post/pose_graph_optimization.html).

### :file_folder: Datasets

`intel.g2o`: real world measurements containing pose-pose constraints only.

`dlr.g2o`: real world measurements containing both pose-pose and pose-landmark constraints.

**Nodes**

`VERTEX_SE2`: 2D pose of the robot, stored as $(x, y, \theta)$.

`VERTEX_XY`: 2D location of the landmark, stored as $(x, y)$.
    
**Edges**

`EDGE_SE2`: constraint between two VERTEX_SE2 (pose) nodes, , stored as $(x, y, \theta)$.
    
`EDGE_SE2_XY`: constraint between a VERTEX_SE2 (pose) node and a VERTEX_XY (landmark) node, stored as $(x, y)$.


### :dog: Usage
```shell
python ./pgo.py
```

> Error while implementing Lie derivative, not sure if the derivation is correct yet.