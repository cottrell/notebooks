"""
various bad ideas ... things blow up quickly without a grid, even with caching
"""
import pandas as pd
import scipy.optimize as so
import functools
import numpy.random as nr
import numpy as np
from mylib import bok
from do import F as F_, F_ni, G, _max_x
F = lambda x: F_(x) + F_ni(x)

# bounds = so.Bounds(0, np.inf, keep_feasible=True) # new in scipy 1.1?
bounds = (0, 1)

min_args = dict(method='L-BFGS-B', tol=1e-8, bounds=(bounds, bounds), options=dict(disp=0))

def terminal_reward(state):
    t, X, Y = state
    assert t == 1
    # use all X, all all available room (not more than X)
    y = Y + G(X)
    return F(X - min(X, y))

def V_star(state):
    t, X, Y = state
    if t == 1:
        return terminal_reward(state)
    alpha_x0 = 0.5
    alpha_y0 = 0.5
    def fun(action):
       return Q(state, action)
    res = so.minimize(fun, (alpha_x0, alpha_y0), **min_args)
    return res

def action_to_xy(action, X, Y):
    alpha_x, alpha_y = action
    x = alpha_x * X
    y = alpha_y * (Y + G(x))
    return x, y

def take_step(state, action):
    # reward too
    t, X, Y = state
    if t == 0:
        raise Exception("terminal state!")
    x, y = action_to_xy(action, X, Y)
    state_ = (t - 1, X - x, Y + G(x) - y)
    return state_

# definitely better way to use dask
import dask
import dask.cache
try:
    _cache
except Exception as e:
    print('init cache')
    _cache = dask.cache.Cache(1e9)
_cache.register()

def Q(state, action):
    return _Q(state, action).compute()

@dask.delayed(pure=True)
def _Q(state, action):
    """
    can also reparam to avoid contraints and keep values in the 0, 1 range
    x = alpha_x * X
    y = alpha_y * Y
    alpha_x, alpha_y in [0, 1]
    """
    action = tuple(action)
    print("CALLING Q({}, {})".format(state, action))
    # minimize this not maximize
    t, X, Y = state
    if t == 1:
        assert action is None, 'No choice for action in last state!'
        result = terminal_reward(state)
    else:
        gamma = 1
        x, y = action_to_xy(action, X, Y)
        reward = F(x - y)
        state_ = take_step(state, action)
        if t == 2:
            # in this case just have reward due to action and terminal state reward
            result = reward + gamma * terminal_reward(state_)
        else:
            def fun(action):
                return Q(state_, action)
            alpha_x0 = 0.5
            alpha_y0 = 0.5
            # watch out, Q is not differentiable (piecewise linear) so maybe trouble
            res = so.minimize(fun, (alpha_x0, alpha_y0), **min_args)
            bok('Q')
            result = reward + gamma * res.fun
    return result

# tests
X = 200000
Y = 0
# print(Q((1, X, Y), None))
# V_star((2, X, Y))

def tax(xs, ys, t, X, Y=0):
    # non recursive definition
    assert len(xs) == len(yx) == len(t)
    reward = list()
    tax = list()
    for i, x, y in zip(range(t), xs, ys):
        print(i, x, y)
        Y = Y + G(x) - y
        X = X - x
        assert x >= 0
        assert y >= 0
        assert Y >= 0
        assert X >= 0
        _tax = F(x - y)
        tax.append(_tax)
        reward.append(x - _tax)
    df = pd.DataFrame(list(zip(xs, ys, tax, reward)))
    df.columns = ['x', 'y', 'tax', 'reward']
    return df

def get_random_sample(t=10, X=1e6):
    # sample yx s.t. sum(ys) == sum([G(x) for x in xs]) and 0 <= y <= Y_t for y in ys
    alpha = (1,) * t
    # sample xs s.t. sum(xs) == X
    xs = nr.dirichlet(alpha, size=1)[0] * X
    taxes = list()
    ys = list()
    Ys = list()
    # initial states
    Y = 0
    y = 0
    n = len(xs)
    for i, x in enumerate(xs):
        Y = G(x) + Y - y
        Ys.append(Y)
        # sample y if not last, else take everythin
        if i == (n - 1):
            y = Y
        else:
            y = nr.rand() * Y # in [0, Y]
        taxes.append(F(x - y))
        ys.append(y)
    df = pd.DataFrame(list(zip(xs, ys, Ys, taxes)), columns=['x', 'y', 'Y', 'tax'])
    return df

# df = get_random_sample(t=10)
# print(df)
# print(df.sum())

def get_tax_distribution():
    N = 100
    data = list()
    for ii, t in enumerate(range(2, 11, 1)):
        print(ii)
        for xx in range(50000, 300000, 50000):
            X = xx * t
            for i in range(N):
                df = get_random_sample(t=t, X=X)
                s = df.tax.sum()
                data.append((t, xx, s))
    data = pd.DataFrame(data, columns=['t', 'X', 'tax'])
    # data = data.set_index(['t', 'X']).sort_index()
    return data

# plot this, not super useful
# data = get_tax_distribution()

# need to solve a constrained optimization at each step
# scipy.optimize.minimize(fun, x0, args=(), method=None, constraints=())
