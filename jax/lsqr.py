#!/usr/bin/env python
"""
Which routines are automatically faster?

The 100 iteration example just for quick check.

If convergence is achieved for these examples (TODO: check) then jax gd cpu is fastest.

Watch out for memory usage overflow and swap. It seems there is a leak.

Loss values look junk.

In [5]: res, df = l.get_times()
{'m': 25498, 'n': 2369, 'seed': 1, 'loss': {'np': 23125.252, 'jnp': 710084500.0, 'jax_gd_gpu': 708441000.0, 'jax_gd_cpu': 708441000.0}, 't': {'np': 6.912585735321045, 'jnp': 11.60724401473999, 'jax_gd_gpu': 3.4716579914093018, 'jax_gd_cpu': 1.740495204925537}}

./lsqr.py
{'m': 25498, 'n': 2369, 'seed': 1, 'loss': {'jnp': 7659.3447, 'jax_gd_gpu': 7724.456, 'jax_gd_cpu': 7724.456, 'np': 7659.3438}, 't': {'jnp': 10.884268999099731, 'jax_gd_gpu': 3.4091343879699707, 'jax_gd_cpu': 1.6997346878051758, 'np': 6.860450983047485}}


"""
import time

import numpy as np
import pandas as pd
import scipy.optimize

import jax
import jax.numpy as jnp


def check_gpu():
    from jax.lib import xla_bridge

    return xla_bridge.get_backend().platform


assert check_gpu() == 'gpu'


def get_data(m, n, seed):
    np.random.seed(seed)
    A = 2 * np.random.rand(m, n).astype(np.float32) - 1
    b = 2 * np.random.rand(m).astype(np.float32) - 1
    u0 = (2 * np.random.rand(n).astype(np.float32) - 1) * 0.01
    return A, b, u0


def get_times(m=25498, n=2369, seed=0):
    A, b, u0 = get_data(m, n, seed)
    res = dict(m=m, n=n, seed=1)
    res['loss'] = dict()
    res['t'] = dict()

    uu = dict()

    # key = 'np_gd'
    # T, losses, uu[key] = run_np_gd(A, b, seed=seed)
    # uu[key] = np.array(uu[key])
    # res['t'][key] = T
    # res['loss'][key] = loss_(uu[key], A, b)
    # print(res)

    for backend in ['gpu', 'cpu']:
        key = f'jax_gd_{backend}'
        print(key)
        T, losses, uu[key] = run(A, b, backend=backend, seed=seed, u0=u0)
        uu[key] = np.array(uu[key])
        res['t'][key] = T
        res['loss'][key] = loss_(uu[key], A, b)
        print(res)

    key = 'jnp'
    print(key)
    T = time.time()
    uu[key] = np.array(jnp.linalg.lstsq(A, b, rcond=None)[0])
    res['t'][key] = time.time() - T
    res['loss'][key] = loss_(uu[key], A, b)
    print(res)

    key = 'np'
    print(key)
    T = time.time()
    uu[key] = np.linalg.lstsq(A, b, rcond=None)[0]
    res['t'][key] = time.time() - T
    res['loss'][key] = loss_(uu[key], A, b)
    print(res)


    uu = {k: v.squeeze() for k, v in uu.items()}
    df = pd.DataFrame(uu)
    return res, df


def loss_(u, A, b):
    return np.sum((A @ u - b) ** 2)


def loss_grad(u, A, b):
    return 2 * (A @ u - b).T @ A


def run_np_gd(A, b, seed=1, n=100, step_size=1e-6, doplot=False):
    np.random.seed(seed)
    u = np.random.randn(A.shape[1])
    losses = list()
    b = b.squeeze()  # we need this for broadcasting reasons
    T = time.time()
    for i in range(n):
        print(i)
        du = loss_grad(u, A, b)
        u = u - step_size * du
        loss = loss_(u, A, b)
        losses.append(loss)
    T = time.time() - T
    losses = np.array(losses)
    if doplot:
        import matplotlib.pyplot as plt

        plt.ion()
        fig = plt.figure(1)
        fig.clf()
        ax_ = fig.subplots(2, 1)
        ax = ax_[0]
        x = np.arange(len(losses))
        y = losses
        ax.plot(x, y, 'o', alpha=0.5)
        ax.set_ylabel('loss')
        ax = ax_[1]
        dy = -np.diff(np.log(losses))
        ax.plot(x[1:], dy, 'o', alpha=0.5)
        ax.set_ylabel('dlog(loss)')
        fig.show()
    return T, losses, u


def run(A, b, n=100, seed=0, step_size=1e-6, doplot=False, backend='gpu', *, u0):
    assert np.ndim(b) == 1
    def loss(u, A, b):
        return jnp.sum((A @ u - b) ** 2)

    loss = jax.jit(loss, backend=backend)

    def update(u, A, b, step_size):
        value, grad = jax.value_and_grad(loss)(u, A, b)
        return value, u - step_size * grad

    update = jax.jit(update, backend=backend)

    key = jax.random.PRNGKey(seed)
    # u = jax.random.normal(key, (A.shape[1], 1)) * 0.01
    u = jax.device_put(u0)
    losses = list()
    update(u, A, b, step_size)  # call once to prime it

    T = time.time()
    for i in range(n):
        loss_, u = update(u, A, b, step_size)
        losses.append(loss_)
    T = time.time() - T
    losses = np.array(losses)
    if doplot:
        import matplotlib.pyplot as plt

        plt.ion()
        fig = plt.figure(1)
        fig.clf()
        ax_ = fig.subplots(2, 1)
        ax = ax_[0]
        x = np.arange(len(losses))
        y = losses
        ax.plot(x, y, 'o', alpha=0.5)
        ax.set_ylabel('loss')
        ax = ax_[1]
        dy = -np.diff(np.log(losses))
        ax.plot(x[1:], dy, 'o', alpha=0.5)
        ax.set_ylabel('dlog(loss)')
        fig.show()
    return T, losses, u

if __name__ == '__main__':
    res, df = get_times()
    print(res)
