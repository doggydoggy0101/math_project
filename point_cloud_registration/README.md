# :robot: Point cloud registration

Numercial examples of blog: [Point cloud registration](https://dgbshien.com/post/point_cloud_registration.html).

### :dog: Usage
```shell
python ./demo.py
```
We showcase four approaches to solve the rotational constraint of the registration problem: linear relaxation, semidefinite relaxation, manifold optimization, and Lie theory.

```shell
---------- Bunny dataset ----------
rng: 134
points 500
ground truth rotation:
 [[-0.8983585  -0.41445738  0.1455235 ]
 [-0.02923889  0.38697643  0.92162592]
 [-0.43828883  0.82369553 -0.35976184]]
ground truth translation: [0.4684641  0.25851681 0.36242912]
projection error: 334.366

Solved by linear relaxation:
estimated rotation:
 [[-0.90358152 -0.41785086  0.0945574 ]
 [-0.11065896  0.44086132  0.89072773]
 [-0.41387804  0.79438149 -0.44459308]]
estimated translation: [0.48346474 0.26137111 0.36449632]
time elapsed: 0.01281 sec
rotation error: 0.10439 (degree)
translation error: 0.01541 (norm)

Solved by semidefinite relaxation:
relaxation is tight: True
estimated rotation:
 [[-0.90072725 -0.42711534  0.07913849]
 [-0.1191557   0.41813925  0.90053399]
 [-0.4177228   0.80170571 -0.42752265]]
estimated translation: [0.48345206 0.26136426 0.36448675]
time elapsed: 0.09605 sec
rotation error: 0.09896 (degree)
translation error: 0.01539 (norm)

Solved by Riemannian gradient descent:
-- rgd: 72 iterations
estimated rotation:
 [[ 0.96463359  0.03428093  0.26135581]
 [ 0.01078965  0.98554111 -0.16909257]
 [-0.26337355  0.16593231  0.95031618]]
estimated translation: [0.50026721 0.27045487 0.37716412]
time elapsed: 0.01466 sec
rotation error: 2.59376 (degree)
translation error: 0.03703 (norm)

Solved by Lie gradient descent:
-- rgd: 72 iterations
estimated rotation:
 [[ 0.96463359  0.03428093  0.26135581]
 [ 0.01078965  0.98554111 -0.16909257]
 [-0.26337355  0.16593231  0.95031618]]
estimated translation: [0.50026721 0.27045487 0.37716412]
time elapsed: 0.42435 sec
rotation error: 2.59376 (degree)
translation error: 0.03703 (norm)
```