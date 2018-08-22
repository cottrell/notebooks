import pandas as pd
import scipy.optimize as so
import functools
import numpy.random as nr
import numpy as np
from mylib import bok
from do import F as F_, F_ni, G, _max_x
F = lambda x: F_(x) + F_ni(x)

# complex one

def F_const(t, X, Y, alphas):
    r = _F_const_full(t, X, Y, alphas)
    return sum(r['tax'])

def _F_const_full(t, X, Y, alphas):
    alphas = np.atleast_2d(np.array(alphas))
    assert alphas.shape[1] == 2
    assert (t - 1) == alphas.shape[0]
    alphas = np.vstack([alphas, [1, 1]])
    tax = list()
    alpha_ys = list()
    alpha_xs = list()
    ys = list()
    xs = list()
    Xs = list()
    Ys = list()
    x = X / t
    for i, (alpha_x, alpha_y) in enumerate(alphas):
        Xs.append(X)
        Ys.append(Y)
        alpha_xs.append(alpha_x)
        alpha_ys.append(alpha_y)
        x = alpha_x * X
        y = alpha_y * min(X, (Y + G(x)))
        xs.append(x)
        ys.append(y)
        tax.append(F(x - y))
        X = X - x
        Y = Y + G(x) - y
        assert X >= 0
        assert Y >= 0
    return dict(tax=tax, xs=xs, ys=ys, Ys=Ys, Xs=Xs, alpha_xs=alpha_xs, alpha_ys=alpha_ys)

# test
t = 3
X = 200000 * t
Y = 0
# r = _F_const_full(t, X, Y, np.array([[.3, .3], [1, 1]]))
def get_var(t, X, n=1000):
    X = X * t
    d = list()
    for i in range(n):
        r = _F_const_full(t, X, Y, nr.rand(t-1, 2))
        d.append(sum(r['tax']))
    d = pd.Series(d)
    s = d.describe()
    return (s['max'] - s['min']) / t

# from pylab import *
# ion()
# 
# def doplot(X):
#     figure(1)
#     clf()
#     df = list()
#     t = 3
#     Y = 0
#     # for X in range(50000, 350000, 50000):
#     for alpha_y in np.linspace(0, 1, 20):
#         r = _F_const_full(t, X * t, Y, np.array([alpha_y, 0]))
#         d = dict(t=t, X=X, Y=Y, alpha_y=alpha_y, tax=sum(r['tax']), tax_=r['tax'], ys=sum(r['ys']), ys_=r['ys'], xs=sum(r['xs']), xs_=r['xs'])
#         df.append(d)
#     df = pd.DataFrame(df)
#     return df
# 
# figure(1)
# clf()
# df = doplot(110000)
# plot(df.alpha_y, df.tax)
# show()
