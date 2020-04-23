import pandas as pd
import scipy.optimize as so
import functools
import numpy.random as nr
import numpy as np
from mylib import bok
from do import F as F_, F_ni, G, _max_x
F = lambda x: F_(x) + F_ni(x)

# simple one first

def F_const(t, X, Y, alpha_ys):
    r = _F_const_full(t, X, Y, alpha_ys)
    return sum(r['tax'])

def _F_const_full(t, X, Y, alpha_ys):
    assert (t - 1) == len(alpha_ys)
    alpha_ys = np.hstack([alpha_ys, 1])
    tax = list() 
    ys = list()
    Xs = list()
    Ys = list()
    x = X / t
    for i, alpha_y in enumerate(alpha_ys):
        Xs.append(X)
        Ys.append(Y)
        y = alpha_y * min(X, (Y + G(x)))
        ys.append(y)
        tax.append(F(x - y))
        X = X - x
        Y = Y + G(x) - y
        assert X >= 0
        assert Y >= 0
    return dict(tax=tax, xs=np.repeat(x, t), ys=ys, Ys=Ys, Xs=Xs, alpha_ys=alpha_ys)

# # test
# t = 2
# X = 200000 * t
# Y = 0
# r = _F_const_full(t, X, Y, [1])
# print(r)

from pylab import *
ion()

def doplot(X):
    figure(1)
    clf()
    df = list()
    t = 3
    Y = 0
    # for X in range(50000, 350000, 50000):
    for alpha_y in np.linspace(0, 1, 20):
        r = _F_const_full(t, X * t, Y, np.array([alpha_y, 0]))
        d = dict(t=t, X=X, Y=Y, alpha_y=alpha_y, tax=sum(r['tax']), tax_=r['tax'], ys=sum(r['ys']), ys_=r['ys'], xs=sum(r['xs']), xs_=r['xs'])
        df.append(d)
    df = pd.DataFrame(df)
    return df

figure(1)
clf()
df = doplot(110000)
plot(df.alpha_y, df.tax)
show()
