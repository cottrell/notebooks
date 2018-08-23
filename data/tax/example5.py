import os
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

def multiplot(force=True):
    t = 2
    dirname = os.path.join(_mydir, 'plots')
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    ioff()
    _max = 350000
    _max_z = _max / 2
    for A in range(10000, _max, 1000):
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
            v = f([alpha_x, alpha_y]) / t
            d.append([alpha_x, alpha_y, v])
    d = pd.DataFrame(d, columns='alpha_x,alpha_y,tax'.split(','))
    df = d.set_index(['alpha_x', 'alpha_y'])['tax'].unstack('alpha_y')
    # figure(num)
    # clf()
    # sns.heatmap(df)

    from mpl_toolkits import mplot3d
    import matplotlib.pyplot as plt
    fig = plt.figure(num)
    fig.clf()
    ax = plt.axes(projection='3d')
    xx, yy, zz = meshgrid_from_df(df)
    ax.plot_wireframe(xx, yy, zz, color='black')
    ax.set_xlabel(df.index.names[0])
    ax.set_ylabel(df.columns.names[0])
    ax.set_title('t = {}, A = {}'.format(t, A))
    if zlim is not None:
        ax.set_zlim(*zlim)
    if filename is not None:
        print('saving {}'.format(filename))
        savefig(filename)
    return d, ax

@curry
def f_opt(t, X, Y, alphas_ravelled):
    alphas = unravel(np.array(alphas_ravelled))
    return sum(_F_const_full(t, X, Y, alphas)['tax'])

def unravel(actions):
    return actions.reshape((int(actions.shape[0] / 2), 2))

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
