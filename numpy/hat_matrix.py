import numpy as np
from numpy.linalg import inv, solve
m = 1000
n = 10

X = np.random.randn(m, n)

XX = X.T @ X

A = inv(XX) @ X.T
B = solve(XX, X.T)

assert np.allclose(A, B)

%timeit _ = inv(XX) @ X.T
%timeit _ = solve(XX, X.T)
