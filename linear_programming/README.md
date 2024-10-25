# :books: Linear programming
Sample code of Linear programming (Fall 2020), National Taiwan Normal University. An introduction to linear program can be found [here](https://dgbshien.com/post/linear_programming.html).

### :notebook: Simplex method
```shell
python ./demo.py
```

We provide 4 example in `demo.py`, all in canonical form.
``` shell
------------- Linear Equation System --------------
x1 +2.0*x2 -2.0*x3 +x4 =1.0
2.0*x1 -1.0*x2 +3.0*x3 +x5 =4.0
x1 +x2 +5.0*x3 +x6 =2.0
-1.0*x1 +2.0*x2 -3.0*x3 =0.0

-------------------- Iteration --------------------
initial system:
[[1 2 -2 1 0 0 1]
 [2 -1 3 0 1 0 4]
 [1 1 5 0 0 1 2]
 [-1 2 -3 0 0 0 0]]

1 iteration:
[[7/5 12/5 0 1 0 2/5 9/5]
 [7/5 -8/5 0 0 1 -3/5 14/5]
 [1/5 1/5 1 0 0 1/5 2/5]
 [-2/5 13/5 0 0 0 3/5 6/5]]

2 iteration:
[[1 12/7 0 5/7 0 2/7 9/7]
 [0 -4 0 -1 1 -1 1]
 [0 -1/7 1 -1/7 0 1/7 1/7]
 [0 23/7 0 2/7 0 5/7 12/7]]

--------------------- Summary ---------------------
iterations: 2
basic variables (index): [1 5 3]
basic feasible solution: [9/7 0 1/7 0 1 0]
optimal: -1.7142857142857144
```