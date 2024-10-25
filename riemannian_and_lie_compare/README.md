# :robot: Riemannian and Lie theory comparison
Numercial examples of blog: [Riemannian and Lie theory comparison](https://dgbshien.com/post/riemannian_lie_compare.html).

### :dog: Special orthogonal manifold
```shell
python ./demo_so3.py
```
We showcase solving rotation estimation problems with Riemannian gradient and Lie derivative, respectively.
```shell
gradient defined by Riemannian manifold structure:
 [[  0.           7.82660583  -0.23057624]
 [ -7.82660583   0.         -23.94096999]
 [  0.23057624  23.94096999   0.        ]]

gradient defined by Lie theory:
 [[  0.           7.82660583  -0.23057624]
 [ -7.82660583   0.         -23.94096999]
 [  0.23057624  23.94096999   0.        ]]
```

### :dog: Special Euclidean manifold
```shell
python ./demo_se3.py
```
We showcase solving point cloud registration problems with Riemannian gradient and Lie derivative, respectively.
```shell
gradient defined by Riemannian manifold structure:
 [[-122.44003401   -2.90654514 -117.7515404    98.13599257]
 [  32.94766592  -92.53706257   25.04435028 -296.39755986]
 [  10.64323376  149.61171356   20.86580791  407.73588452]
 [   0.            0.            0.            0.        ]]

gradient defined by Lie theory:
 [[-122.44003401   -2.90654514 -117.7515404    98.13599257]
 [  32.94766592  -92.53706257   25.04435028 -296.39755986]
 [  10.64323376  149.61171356   20.86580791  407.73588452]
 [   0.            0.            0.            0.        ]]
```