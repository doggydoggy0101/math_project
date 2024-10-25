# Jacobian
Define the Jacobians in `least_squares.py`.

## pose-pose constraint

- pose $X_i=\begin{pmatrix}R_i&t_i\\0^\top&1\end{pmatrix}\in\text{SE}(2)$, vectorized as $(t_{i}, \theta_{i})\in\mathbb{R}^3$
- pose $X_j=\begin{pmatrix}R_j&t_j\\0^\top&1\end{pmatrix}\in\text{SE}(2)$, vectorized as $(t_{j}, \theta_{j})\in\mathbb{R}^3$
- ground truth $\hat{X}_{ij}=\begin{pmatrix}\hat{R}_{ij}&\hat{t}_{ij}\\0^\top&1\end{pmatrix}\in\text{SE}(2)$, vectorized as $(\hat{t}_{ij}, \hat{\theta}_{ij})\in\mathbb{R}^3$

### Euclidean approach

residual function, [[1]](#GKS10) Equation (30)
$$
f:\text{SE}(2)\times\text{SE}(2)\to\mathbb{R}^3\ ;\ \ 
f(X_i,X_j)=\begin{pmatrix}\hat{R}_{ij}^\top(R_i^\top(t_j-t_i)-\hat{t}_{ij})\\(\theta_j-\theta_i)-\hat{\theta}_{ij}\end{pmatrix}
$$

Jacobian with respective to vectorized $X_i$, [[1]](#GKS10) Equation (32)
$$
\begin{pmatrix}
\frac{\partial f}{\partial t_i}&
\frac{\partial f}{\partial \theta_i}
\end{pmatrix}=
\begin{pmatrix}
-\hat{R}_{ij}^\top R_i^\top&\hat{R}_{ij}^\top \frac{\partial R_i^\top}{\partial\theta_i}(t_j-t_i)\\
0^\top&-1
\end{pmatrix}
$$

Jacobian with respective to vectorized $X_j$, [[1]](#GKS10) Equation (33)
$$
\begin{pmatrix}
\frac{\partial f}{\partial t_j}&
\frac{\partial f}{\partial \theta_j}
\end{pmatrix}=
\begin{pmatrix}
\hat{R}_{ij}^\top R_i^\top&0\\
0^\top&1
\end{pmatrix}
$$

### Lie theory approach

residual function, [[2]](#GZL17) Equation (9.4)
$$
f:\text{SE}(2)\times\text{SE}(2)\to\mathbb{R}^3\ ;\ \ 
f(X_i,X_j)=X_i^{-1}X_j\ominus\hat{X}_{ij}=\text{Log}(\hat{X}_{ij}^{-1}X_i^{-1}X_j)
$$

Jacobian with respective to vectorized $X_i$,
$$
\begin{aligned}
J^{\text{Log}(\hat{X}_{ij}^{-1}X_i^{-1}X_j)}_{X_i}&=J^{\text{Log}(\hat{X}_{ij}^{-1}X_i^{-1}X_j)}_{\hat{X}_{ij}^{-1}X_i^{-1}X_j}\cdot
J^{\hat{X}_{ij}^{-1}X_i^{-1}X_j}_{X_i^{-1}X_j}\cdot
J^{X_i^{-1}X_j}_{X_j^{-1}X_i}\cdot
J^{X_j^{-1}X_i}_{X_i}\cdot\\
&=-J_r^{-1}(\text{Log}(\hat{X}_{ij}^{-1}X_i^{-1}X_j))\text{Ad}_{X^{-1}_jX_i}
\end{aligned}
$$

Jacobian with respective to vectorized $X_j$,
$$
\begin{aligned}
J^{\text{Log}(\hat{X}_{ij}^{-1}X_i^{-1}X_j)}_{X_j}&=J^{\text{Log}(\hat{X}_{ij}^{-1}X_i^{-1}X_j)}_{\hat{X}_{ij}^{-1}X_i^{-1}X_j}\cdot
J^{\hat{X}_{ij}^{-1}X_i^{-1}X_j}_{X_i}\\
&=J_r^{-1}(\text{Log}(\hat{X}_{ij}^{-1}X_i^{-1}X_j))
\end{aligned}
$$


> $J_r(\cdot)$ and $\text{Ad}_{(\cdot)}$ can be found at [[3]](#SDA18) Equation (163) and (159), respectively.


## pose-landmark constraint

TBD.


### Reference

<a id="GKS10">[1]</a> 
Grisetti, G., Kümmerle, R., Stachniss, C., & Burgard, W. (2010). A tutorial on graph-based SLAM. IEEE Intelligent Transportation Systems Magazine, 2(4), 31-43.

<a id="GZL17">[2]</a> 
Gao, X., Zhang, T., Liu, Y., & Yan, Q. (2017). 14 lectures on visual SLAM: from theory to practice. Publishing House of Electronics Industry, 206-234.

<a id="SDA18">[3]</a> 
Sola, J., Deray, J., & Atchuthan, D. (2018). A micro Lie theory for state estimation in robotics. arXiv preprint arXiv:1812.01537.