import pandas as pd
import scipy.optimize as so
import functools
import numpy.random as nr
import numpy as np
from mylib import bok
from do import F as F_, F_ni, G, _max_x
F = lambda x: F_(x) + F_ni(x)

def total_tax_with_optimal_terminal_state_constant_income(t, X, Y, actions):
    """ actions should be an (n-1) x 1 np array """
    r = get_tax_pension_income_optimal_terminal_state_constant_income(t, X, Y, actions)
    return sum(r['tax'])

def get_tax_pension_income_optimal_terminal_state_constant_income(t, X, Y, actions):
    """ no choice of x, just y """
    assert (t - 1) == len(actions)
    assert len(actions.shape) == 1
    actions = np.hstack([actions, [np.inf]]) # apply_optimal_...
    xs = np.repeat([X / t], t)
    return get_tax_pension_income_fixed_x(t, X, Y, xs, actions)

# test
# t = 2
# X = 200000
# Y = 0
# actions = np.array([1])
# r = get_tax_pension_income_optimal_terminal_state_constant_income(t, X, Y, actions)

def total_tax_with_optimal_terminal_state(t, X, Y, actions):
    """
    actions should prob be an (n-1) x 2 np array
    """
    r = get_tax_pension_income_optimal_terminal_state(t, X, Y, actions)
    return sum(r['tax'])

def get_tax_pension_income_optimal_terminal_state(t, X, Y, actions):
    assert (t - 1) == len(actions)
    actions = apply_optimal_terminal_action(actions)
    return get_tax_pension_income(t, X, Y, actions)

def get_tax_pension_income_fixed_x(t, X, Y, xs, actions):
    assert t == len(actions)
    tax = list() 
    ys = list() # pension
    Xs = list()
    Ys = list()
    alpha_ys = list()
    for i, (x, action) in enumerate(zip(xs, actions)):
        Xs.append(X)
        Ys.append(Y)
        alpha_y = action_to_zeroone(action) # this will work in both cases
        alpha_ys.append(alpha_y)
        y = alpha_y * min(X, (Y + G(x)))
        ys.append(y)
        tax.append(F(x - y))
        X = X - x
        Y = Y + G(x) - y
        assert X >= 0
        assert Y >= 0
    return dict(tax=tax, xs=xs, ys=ys, Ys=Ys, Xs=Xs, alpha_ys=alpha_ys)

def get_tax_pension_income(t, X, Y, actions):
    """
    just the calc given alphas
    avoid recursion
    last step can be sub-optimal, if you want optimal set alpha[-1] = 1
    """
    assert t == len(actions)
    tax = list() 
    xs = list() # gross
    ys = list() # pension
    Xs = list()
    Ys = list()
    alpha_xs = list()
    alpha_ys = list()
    for i, action in enumerate(actions):
        Xs.append(X)
        Ys.append(Y)
        alpha_x, alpha_y = action_to_zeroone(action)
        alpha_xs.append(alpha_x)
        alpha_ys.append(alpha_y)
        x, y = action_to_xy(action, X, Y)
        xs.append(x)
        ys.append(y)
        tax.append(F(x - y))
        print(action, X)
        X = X - x
        print('after', X, x)
        Y = Y + G(x) - y
        assert X >= 0
        assert Y >= 0
    if alpha_x == 1:
        assert X == 0
    # note that Y might not be zero because you can not draw down more than X
    return dict(tax=tax, xs=xs, yx=ys, Ys=Ys, Xs=Xs, alpha_xs=alpha_xs, alpha_ys=alpha_ys)

def action_to_zeroone(action):
    # tuple or array
    action = 1. / (1. + np.exp(-action))
    assert (0 <= action).all()
    assert (action <= 1).all()
    return action

def action_to_y(action, X, Y):
    # not sure if makes sense for array of actions
    alpha_y = action_to_zeroone(action)
    x = alpha_x * X
    y = alpha_y * min(X, (Y + G(x)))
    return x, y

def action_to_xy(action, X, Y):
    # not sure if makes sense for array of actions
    alpha_x, alpha_y = action_to_zeroone(action)
    x = alpha_x * X
    y = alpha_y * min(X, (Y + G(x)))
    return x, y

def apply_optimal_terminal_action(actions):
    return np.vstack([actions, [np.inf, np.inf]])

# # test
# t = 3
# X = t * 200000
# Y = 0
# actions = nr.rand(t, 2)
# res = get_tax_pension_income(t, X, Y, actions)
# 
# # test
# actions = nr.randn(t - 1, 2) # actions are in the reals, alphas are in [0, 1]
# s = get_tax_pension_income_optimial_terminal_state(t, X, Y, actions)
# ss = total_tax_with_optimal_terminal_state(t, X, Y, actions)

def unravel(actions):
    n = actions.shape[0]
    return actions.reshape((int(n / 2), 2))

def optimal_allocation(t, X, Y, init_actions=None):
    if init_actions is None:
        init_actions = nr.randn((t - 1) * 2)
    else:
        orig = init_actions.copy()
        init_actions = init_actions.ravel()
        assert (unravel(init_actions) == orig).all()
    min_args = dict(method='Nelder-Mead', tol=1e-12, options=dict(disp=True))
    # function needs to take 1d arg
    # actions.ravel() to get 1d rep
    def fun(actions):
        return total_tax_with_optimal_terminal_state(t, X, Y, unravel(actions))
    res = so.minimize(fun, init_actions, **min_args)
    actions = apply_optimal_terminal_action(unravel(res.x))
    alpha = action_to_zeroone(actions)
    res.update(dict(actions=actions, alpha=alpha))
    return res

def uniform_to_actions(alpha):
    return np.log(alpha) - np.log(1 - alpha)

def optimal_allocation_with_random_inits(t, X, Y, n=10):
    # grid is too large to sample, just be random in uniform space
    res = list()
    for i in range(n):
        print(i)
        alpha = nr.rand(t - 1, 2)
        actions = np.log(alpha) - np.log(1 - alpha)
        r = optimal_allocation(t, X, Y, init_actions=actions)
        res.append(r)
    return res

# r = optimal_allocation_with_random_inits(t, X, Y, n=10)
# r = pd.DataFrame(r)

import skopt
from skopt import Optimizer
from skopt.learning import GaussianProcessRegressor
from skopt.space import Real
from sklearn.externals.joblib import Parallel, delayed

# pickle problems
import toolz
@toolz.curry
def _fun(t, X, Y, alpha):
    actions = unravel(uniform_to_actions(np.array(alpha)))
    return total_tax_with_optimal_terminal_state(t, X, Y, actions)

@toolz.curry
def _fun_constant_income(t, X, Y, alpha):
    actions = uniform_to_actions(np.array(alpha))
    return total_tax_with_optimal_terminal_state_constant_income(t, X, Y, actions)

def optimal_allocation_with_skopt(t, X, Y, n=10, n_parallel=4, const_income=True):
    # [0, 1]
    nn = 2
    opt_fun = _fun
    if const_income:
        nn = 1
        opt_fun = _fun_constant_income
    dimensions = [Real(0, 1)] * nn * (t - 1)
    optimizer = skopt.Optimizer(
            dimensions, base_estimator='gp', random_state=1
            # n_random_starts=None, n_initial_points=10, acq_func='gp_hedge', acq_optimizer='auto', acq_func_kwargs=None, acq_optimizer_kwargs=None
            )
    # fun = functools.partial(_fun, t, X, Y)
    fun = opt_fun(t, X, Y)
    if n_parallel <= 1:
        print('not parallel')
        for i in range(n):
                suggested = optimizer.ask()
                y = fun(suggested)
                optimizer.tell(suggested, y)
                print('iteration: {}, {}, {}'.format(i, suggested, y))
    else:
        # something not working here
        print('parallel')
        n_left = n
        for i in range(0, n, max(n_parallel, 1)):
            suggested = optimizer.ask(n_points=min(n_left, n_parallel))
            n_left -= n_parallel
            print(n_left)
            y = Parallel()(delayed(fun)(x) for x in suggested)
            optimizer.tell(suggested, y)
            print('iteration: {}, {}, {}, {}'.format(i, suggested, y, action_to_zeroone(np.array(suggested))))
    print('min is', min(optimizer.yi))
    return optimizer

t = 2
X = 100000 * t
Y = 0
test = functools.partial(optimal_allocation_with_skopt, t, X, Y)
# see Xi and yi

actions = uniform_to_actions(np.linspace(0, 1, 100))
from pylab import *
figure()
fs = [total_tax_with_optimal_terminal_state_constant_income(t, X, Y, np.array([action])) for action in actions]
