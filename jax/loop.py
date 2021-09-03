import matplotlib.pyplot as plt

plt.ion()
import numpy as np
import pandas as pd

import jax
import jax.numpy as jnp
import jax.experimental.optimizers

alpha = 1e-1

DEFAULT_SEED = 0
DEFAULT_M = 100

def get_data(m=DEFAULT_M, seed=DEFAULT_SEED):
    np.random.seed(seed)
    y = np.random.randn(m, 1).astype(np.float32)
    return y


@jax.jit
def loss_fn_with_aux(theta, y):
    loss_reg = jnp.sum(theta ** 2)
    loss_data = jnp.sum((y - theta) ** 2)
    loss = loss_data + alpha * loss_reg
    return loss, dict(loss_reg=loss_reg, loss_data=loss_data)


@jax.jit
def loss_fn_no_aux(theta, y):
    loss_reg = jnp.sum(theta ** 2)
    loss_data = jnp.sum((y - theta) ** 2)
    loss = loss_data + alpha * loss_reg
    return loss



def basic_loop(fig=1, step_size=1e-2, n_plot=100, n_steps=1000):

    y = get_data()
    m = y.shape[0]

    key = jax.random.PRNGKey(0)
    theta = jax.random.normal(key, (m, 1))

    @jax.jit
    def step(theta, y):
        (value, aux), grad = jax.value_and_grad(loss_fn_with_aux, has_aux=True)(theta, y)
        # return value, [x - step_size * dx for x, dx in zip(params, grads)]
        return aux, theta - step_size * grad

    ldata = list()
    plot_period = n_steps // n_plot
    for i in range(n_steps):
        aux, theta = step(theta, y)
        if i % plot_period == 0:
            aux = {k: v.item() for k, v in aux.items()}
            ldata.append(aux)

    ldata = pd.DataFrame(ldata)
    fig = plt.figure(fig)
    fig.clf()
    ax = fig.subplots(1)
    ldata.plot(ax=ax)
    ax.set_title('basic_loop')


def adam_loop(fig=2, init_sigma=1e-4, learning_rate=1e-2, n_plot=10000, n_steps=10000, seed=DEFAULT_SEED):

    y = get_data()
    m = y.shape[0]

    np.random.seed(seed)

    key = jax.random.PRNGKey(seed)
    theta = jax.random.uniform(key, (m, 1)) * init_sigma
    opt_init, opt_update, opt_get_params = jax.experimental.optimizers.sgd(learning_rate)
    opt_state = opt_init(theta)

    @jax.jit
    def step(step, opt_state):
        (value, aux), grads = jax.value_and_grad(loss_fn_with_aux, has_aux=True)(opt_get_params(opt_state), y)
        # value, grads = jax.value_and_grad(loss_fn_no_aux, has_aux=False)(opt_get_params(opt_state), y)
        opt_state = opt_update(step, grads, opt_state)
        return aux, opt_state

    for i in range(n_steps):
        value, opt_state = step(i, opt_state)

    ldata = list()
    plot_period = n_steps // n_plot
    for i in range(n_steps):
        aux, opt_state = step(i, opt_state)
        if i % plot_period == 0:
            aux = {k: v.item() for k, v in aux.items()}
            ldata.append(aux)

    ldata = pd.DataFrame(ldata)
    fig = plt.figure(fig)
    fig.clf()
    ax = fig.subplots(1)
    ldata.plot(ax=ax)
    ax.set_title('adam')
