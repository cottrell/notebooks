"""
Which routines are automatically faster?

The 100 iteration example just for quick check.

If convergence is achieved for these examples (TODO: check) then jax gd cpu is fastest.

In [42]: reload(l); res, df = l.get_times()
{'m': 25498, 'n': 2369, 'seed': 1, 'loss': {'np': 23125.252}, 't': {'np': 9.406081438064575}}
{'m': 25498, 'n': 2369, 'seed': 1, 'loss': {'np': 23125.252, 'jnp': 23125.25}, 't': {'np': 9.406081438064575, 'jnp': 9.40992021560669}}
{'m': 25498, 'n': 2369, 'seed': 1, 'loss': {'np': 23125.252, 'jnp': 23125.25, 'jax_gd_gpu': 23128.648}, 't': {'np': 9.406081438064575, 'jnp': 9.40992021560669, 'jax_gd_gpu': 2.3344671726226807}}
{'m': 25498, 'n': 2369, 'seed': 1, 'loss': {'np': 23125.252, 'jnp': 23125.25, 'jax_gd_gpu': 23128.648, 'jax_gd_cpu': 23128.648}, 't': {'np': 9.406081438064575, 'jnp': 9.40992021560669, 'jax_gd_gpu': 2.3344671726226807, 'jax_gd_cpu': 1.7780954837799072}}
"""
import time

import numpy as np
import pandas as pd

import jax
import jax.numpy as jnp


def check_gpu():
    from jax.lib import xla_bridge

    return xla_bridge.get_backend().platform


assert check_gpu() == 'gpu'


def get_data(m, n, seed):
    np.random.seed(seed)
    A = np.random.randn(m, n).astype(np.float32)
    b = np.random.randn(m, 1).astype(np.float32)
    return A, b


def get_times(m=25498, n=2369, seed=1):
    A, b = get_data(m, n, seed)
    res = dict(m=m, n=n, seed=1)
    res['loss'] = dict()
    res['t'] = dict()

    uu = dict()

    T = time.time()
    uu['np'] = np.linalg.lstsq(A, b, rcond=None)[0]
    res['t']['np'] = time.time() - T
    res['loss']['np'] = loss_(uu['np'], A, b)
    print(res)

    T = time.time()
    uu['jnp'] = np.array(jnp.linalg.lstsq(A, b, rcond=None)[0])
    res['t']['jnp'] = time.time() - T
    res['loss']['jnp'] = loss_(uu['jnp'], A, b)
    print(res)

    for backend in ['gpu', 'cpu']:
        key = f'jax_gd_{backend}'
        T, losses, uu[key] = run(A, b, backend=backend, seed=seed)
        uu[key] = np.array(uu[key])
        res['t'][key] = T
        res['loss'][key] = loss_(uu[key], A, b)
        print(res)

    uu = {k: v.squeeze() for k, v in uu.items()}
    df = pd.DataFrame(uu)
    return res, df


def loss_(u, A, b):
    return np.sum((A @ u - b) ** 2)


def run(A, b, n=100, seed=1, step_size=1e-6, doplot=False, backend='gpu'):
    def loss(u, A, b):
        return jnp.sum((A @ u - b) ** 2)

    loss = jax.jit(loss, backend=backend)

    def update(u, A, b, step_size):
        value, grad = jax.value_and_grad(loss)(u, A, b)
        return value, u - step_size * grad

    update = jax.jit(update, backend=backend)

    key = jax.random.PRNGKey(seed)
    u = jax.random.normal(key, (A.shape[1], 1)) * 0.01
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
