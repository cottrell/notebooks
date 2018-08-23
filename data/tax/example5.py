import os
import pprint
from pylab import *
import seaborn as sns
ion()
from toolz import curry
import pandas as pd
import scipy.optimize as so
import functools
import numpy.random as nr
import numpy as np
from mylib import bok
import mylib.plotting as plotting
from do import F as F_, F_ni, G, _max_x
import webbrowser
F = lambda x: F_(x) + F_ni(x)
# x and y
_mydir = os.path.realpath(os.path.dirname(__file__))

gamma = 0.02

_bounds_errors = True

import contextlib
@contextlib.contextmanager
def with_bounds_errors_off():
    global _bounds_errors
    _bounds_errors = False
    yield
    _bounds_errors = True

def multiplot(force=True, step=1000):
    t = 2
    dirname = os.path.join(_mydir, 'plots')
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    ioff()
    _max = 350000
    _max_z = _max / 2
    for A in range(10000, _max, step):
        # ordering hack
        filename = os.path.join(dirname, 'wireframe_t={}_A={:07}.png'.format(t, A))
        if force or not os.path.exists(filename):
            doplot(t=t, A=A, filename=filename) # , zlim=[0, _max_z])
    gif = os.path.join(dirname, 'wireframe_t={}.gif'.format(t))
    pngs = os.path.join(dirname, 'wireframe_t={}_A=*.png'.format(t))
    cmd = 'cd {} && convert -loop 0 -delay 10 {} {}'.format(dirname, pngs, gif)
    print('running: {}'.format(cmd))
    os.system(cmd)
    # webbrowser.open('file://{}'.format(gif)) # opens in preview ugh
    ion()

def doplot(t=2, A=200000, zlim=None, filename=None, num=1):
    assert t == 2, 'will not work otherwise'
    X = A * t
    Y = 0
    f = f_opt(t, X, Y)
    d = list()
    n = 20
    for alpha_x in linspace(0, 1, n + 1):
        for alpha_y in linspace(0, 1, n + 1):
            v = f([alpha_x, alpha_y])
            d.append([alpha_x, alpha_y, v])
    d = pd.DataFrame(d, columns='alpha_x,alpha_y,tax'.split(','))
    df = d.set_index(['alpha_x', 'alpha_y'])['tax'].unstack('alpha_y')
    # df = df.sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=False)
    # figure(num)
    # clf()
    # sns.heatmap(df)

    from mpl_toolkits import mplot3d
    import matplotlib.pyplot as plt
    fig = plt.figure(num)
    fig.clf()
    ax = plt.axes(projection='3d')
    ax.view_init(None, 300)
    xx, yy, zz = plotting.meshgrid_from_df(df)
    ax.plot_wireframe(yy, xx, zz, alpha=0.75)
    ax.set_ylabel(df.index.names[0])
    ax.set_xlabel(df.columns.names[0])
    ax.set_zlabel('annualized tax')
    ax.set_title('t = {}, A = {}'.format(t, A))
    if zlim is not None:
        ax.set_zlim(*zlim)
    if filename is not None:
        print('saving {}'.format(filename))
        savefig(filename)
    return d, ax

def doplot2(t=3, alpha_y=[0.5, 0.5], A=200000, zlim=None, filename=None, num=1):
    # keep alpha_y const, doesn't matter so much
    assert t == 3, 'will not work otherwise'
    X = A * t
    Y = 0
    f = f_opt(t, X, Y)
    d = list()
    n = 20
    for alpha_x0 in linspace(0, 1, n + 1):
        for alpha_x1 in linspace(0, 1, n + 1):
            v = f([alpha_x0, alpha_y[0], alpha_x1, alpha_y[1]])
            d.append([alpha_x0, alpha_x1, v])
    d = pd.DataFrame(d, columns='alpha_x0,alpha_x1,tax'.split(','))
    df = d.set_index(['alpha_x0', 'alpha_x1'])['tax'].unstack('alpha_x1')

    from mpl_toolkits import mplot3d
    import matplotlib.pyplot as plt
    fig = plt.figure(num)
    fig.clf()
    ax = plt.axes(projection='3d')
    ax.view_init(None, 300)
    xx, yy, zz = plotting.meshgrid_from_df(df)
    ax.plot_wireframe(yy, xx, zz, alpha=0.75)
    ax.set_ylabel(df.index.names[0])
    ax.set_xlabel(df.columns.names[0])
    ax.set_zlabel('annualized tax')
    ax.set_title('t = {}, A = {}, alpha_y={}'.format(t, A, alpha_y))
    if zlim is not None:
        ax.set_zlim(*zlim)
    if filename is not None:
        print('saving {}'.format(filename))
        savefig(filename)
    return d, ax

# these should work with more than two
@curry
def f_opt(t, X, Y, alphas_ravelled):
    alphas = unravel(np.array(alphas_ravelled))
    # return sum(_F_const_full(t, X, Y, alphas)['tax_annualized'])
    return sum(_F_const_full(t, X, Y, alphas)['tax_pv_annualized'])

def unravel(actions):
    return actions.reshape((int(actions.shape[0] / 2), 2))

@curry
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
        X = X - x
        Y = Y + G(x)
        y = alpha_y * min(x, Y) # was a bug (X) before!
        Y = Y - y
        xs.append(x)
        ys.append(y)
        tax.append(F(x - y))
        if _bounds_errors:
            assert X >= 0
            assert Y >= 0
        else:
            pass
            # if X < 0:
            #     print('WARNING: X = {} >= 0'.format(X))
            # if Y < 0:
            #     print('WARNING: Y = {} >= 0'.format(Y))
    # as a check, final state
    Xs.append(X)
    Ys.append(Y)
    tax_pv = tax / np.power(1 + gamma, np.arange(0, len(tax)))
    return dict(tax=tax, tax_pv=tax_pv, xs=xs, ys=ys, Ys=Ys, Xs=Xs, alpha_xs=alpha_xs, alpha_ys=alpha_ys, tax_annualized=sum(tax) / t, tax_pv_annualized=sum(tax_pv) / t)

def test_opt(t=2, A=210000, Y=0):
    X = A * t
    f = f_opt(t, X, Y)
    with with_bounds_errors_off() as e:
        init = [0] * 2 * (t - 1)
        # init = [1] * 2 * (t - 1)
        # init = [0.5] * 2 * (t - 1)
        # init = nr.rand(2 * (t - 1))
        # res = so.minimize(f, init, method='Nelder-Mead', bounds=[(0, 1), (0, 1)], options=dict(xatol=0.000001, fatol=0.01, disp=True))
        res = so.minimize(f, init, method='L-BFGS-B', bounds=[(0, 1), (0, 1)] * (t -1), options=dict(approx_grad=True, epsilon=.001, xatol=0.000001, fatol=0.01, disp=True))
    alphas = pd.DataFrame(unravel(np.minimum(1, np.maximum(0, res.x))), columns=['alpha_x', 'alpha_y'])
    r = _F_const_full(t, X, Y, alphas)
    res.update(dict(r=r, alphas=alphas))
    print('fun: {}'.format(res.fun))
    for k in sorted(r.keys()):
        print(k, r[k])
    return res

# skopt.gp_minimize(f, [skopt.space.Real(0, 1)] * 2, noise=0, kappa=10, n_calls=100, n_random_starts=10)
