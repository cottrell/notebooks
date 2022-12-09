import pandas as pd
import jax
import jax.numpy as jnp
import numpy as np
import jax.experimental
import jax.experimental.optimizers

DEFAULT_SEED = 0
DEFAULT_M = 100
DEFAULT_N = 50
DEFAULT_STEP_SIZE = 1e-1
DEFAULT_ALPHA = 1e-6

def find_problem(n_steps=100, opt='sgd', step_size=DEFAULT_STEP_SIZE, alpha=DEFAULT_ALPHA, max_iter=1000):

    X, y  = get_data()
    theta = get_initial_param()


    @jax.jit
    def step(step, opt_state):
        (value, aux), grads = jax.value_and_grad(loss_fn_with_aux, has_aux=True)(opt_get_params(opt_state), X, y, alpha)
        opt_state = opt_update(step, grads, opt_state)
        return (value, aux), grads, opt_state

    for i in range(max_iter):
        optimizer = getattr(jax.experimental.optimizers, opt)
        opt_init, opt_update, opt_get_params = optimizer(step_size)
        opt_state = opt_init(theta)
        for j in range(n_steps):
            (value, aux), grads, opt_state = step(j, opt_state)
            aux['step'] = j
            print(aux, opt_state, grads )
            if not jnp.isfinite(grads).all():
                print('found bad step_size')
                return dict(grads=grads, step_size=step_size, step=j)
        step_size *= 2
    print(f'did not find bad step_size in {max_iter} runs')
    return dict(step_size=step_size)





# custom
from jax.experimental.optimizers import optimizer, make_schedule, Optimizer

@optimizer
def sgd_custom(step_size):
  """Construct optimizer triple for stochastic gradient descent but with some dynamic step_size thing.

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to positive scalar.

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  # step_size = make_schedule(step_size)
  def init(x0, loss0=None, step_size0=step_size):
      if loss0 is None:
          loss0 = np.Inf
      return x0, loss0, step_size0

  def update(i, g_loss, state):
      g, loss = g_loss
      # this breaks the api to some extent, now need to pass in value with gradients
      x, prev_loss, step_size = state
      if loss / prev_loss > 1.1:
          step_size *= 0.5
      x =  x - step_size(i) * g
      return x, loss, step_size

  def get_params(state):
      x, _, _ = state
      return x

  return Optimizer(init, update, get_params)

@optimizer
def adam(step_size, b1=0.9, b2=0.999, eps=1e-8):
  """Construct optimizer triple for Adam.

  Args:
    step_size: positive scalar, or a callable representing a step size schedule
      that maps the iteration index to positive scalar.
    b1: optional, a positive scalar value for beta_1, the exponential decay rate
      for the first moment estimates (default 0.9).
    b2: optional, a positive scalar value for beta_2, the exponential decay rate
      for the second moment estimates (default 0.999).
    eps: optional, a positive scalar value for epsilon, a small constant for
      numerical stability (default 1e-8).

  Returns:
    An (init_fun, update_fun, get_params) triple.
  """
  step_size = make_schedule(step_size)
  def init(x0):
    m0 = jnp.zeros_like(x0)
    v0 = jnp.zeros_like(x0)
    return x0, m0, v0
  def update(i, g, state):
    x, m, v = state
    m = (1 - b1) * g + b1 * m  # First  moment estimate.
    v = (1 - b2) * jnp.square(g) + b2 * v  # Second moment estimate.
    mhat = m / (1 - jnp.asarray(b1, m.dtype) ** (i + 1))  # Bias correction.
    vhat = v / (1 - jnp.asarray(b2, m.dtype) ** (i + 1))
    x = x - step_size(i) * mhat / (jnp.sqrt(vhat) + eps)
    return x, m, v
  def get_params(state):
    x, _, _ = state
    return x
  return init, update, get_params
#

def get_data(m=DEFAULT_M, n=DEFAULT_N, seed=DEFAULT_SEED):
    np.random.seed(seed)
    X = np.random.randn(m, n).astype(np.float32)
    # w = np.random.randn(m, 1).astype(np.float32)
    y = 1 / (np.abs(0.5 - X[:, 0] ** 4 - X[:, 1] ** 4) + 0.1)
    return X, y

def get_initial_param(n=DEFAULT_N, seed=DEFAULT_SEED):
    key = jax.random.PRNGKey(DEFAULT_SEED)
    theta = jax.random.uniform(key, (n, 1)) * 1e-4
    return theta

@jax.jit
def loss_fn_with_aux(theta, X, y, alpha):
    loss_reg = jnp.sum(theta ** 2)
    loss_data = jnp.sum((y - X @ theta) ** 2)
    loss = loss_data + alpha * loss_reg
    return loss, dict(loss=loss, loss_reg=loss_reg, loss_data=loss_data)

def run_optimizer(n_steps=1000, n_plot=100, opt='sgd_custom', step_size=DEFAULT_STEP_SIZE, alpha=DEFAULT_ALPHA):

    X, y  = get_data()
    theta = get_initial_param()

    optimizer = getattr(jax.experimental.optimizers, opt, globals()[opt])
    opt_init, opt_update, opt_get_params = optimizer(step_size)
    opt_state = opt_init(theta)

    @jax.jit
    def step(step, opt_state):
        (value, aux), grads = jax.value_and_grad(loss_fn_with_aux, has_aux=True)(opt_get_params(opt_state), X, y, alpha)
        # assert jnp.isfinite(grads).all()
        # value, grads = jax.value_and_grad(loss_fn_no_aux, has_aux=False)(opt_get_params(opt_state), y)
        opt_state = opt_update(step, (grads, value), opt_state)
        return aux, opt_state
    # return locals()

    df = list()
    plot_period = max(1, n_steps // n_plot)
    for i in range(n_steps):
        aux, opt_state = step(i, opt_state)
        print(aux)
        if i % plot_period == 0:
            aux = {k: v.item() for k, v in aux.items()}
            aux['step'] = i
            df.append(aux)
    if i % plot_period != 0:  # always include last one
        aux = {k: v.item() for k, v in aux.items()}
        df.append(aux)
    df = pd.DataFrame(df)
    return dict(df=df, theta=theta)

def doplot(N=1000):
    df = list()
    for k in ['sgd']: # , 'adam']:
        d = run_optimizer(opt=k, n_plot=N, n_steps=N)
        df_ = d['df']
        df_.columns = pd.MultiIndex.from_tuples([(x, k) for x in df_.columns])
        df.append(df_)
    df = pd.concat(df, axis=1)

    import matplotlib.pyplot as plt
    plt.ion()
    fig = plt.figure(1)
    fig.clf()
    ax_ = fig.subplots(1, 3)
    for i, k in enumerate(['loss', 'loss_data', 'loss_reg']):
        ax = ax_[i]
        df[k].plot(ax=ax)
        ax.set_title(k)
    fig.show()
    return locals()
