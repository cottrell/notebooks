import matplotlib.pyplot as plt

plt.ion()
import numpy as np
import pandas as pd

import jax
import jax.numpy as jnp


@jax.jit
def loss(theta, y):
    loss_reg = jnp.sum(theta ** 2)
    loss_data = jnp.sum((y - theta) ** 2)
    loss = loss_data + alpha * loss_reg
    return loss, dict(loss_reg=loss_reg, loss_data=loss_data)


m = 100
key = jax.random.PRNGKey(0)
theta = jax.random.normal(key, (m, 1))
y = np.random.randn(m, 1).astype(np.float32)
alpha = 1e-2
step_size = 1e-2

# test
(value, aux), grad = jax.value_and_grad(loss, has_aux=True)(theta, y)


@jax.jit
def update(theta, y):
    (value, aux), grad = jax.value_and_grad(loss, has_aux=True)(theta, y)
    # return value, [x - step_size * dx for x, dx in zip(params, grads)]
    return aux, theta - step_size * grad


ldata = list()
n_plot = 100
n_steps = 1000
plot_period = n_steps // n_plot
for i in range(n_steps):
    aux, theta = update(theta, y)
    if i % plot_period == 0:
        aux = {k: v.item() for k, v in aux.items()}
        ldata.append(aux)

ldata = pd.DataFrame(ldata)
fig = plt.figure(1)
fig.clf()
ax = fig.subplots(1)
ldata.plot(ax=ax)
