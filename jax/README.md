# 2022-11

How to remember things after a pause:

You can usually just use vanilla jax.

Haiku is mostly aimed at addressing the problem of keeping initializers and
models in sync which can get tricky if you are trying out a lof of different
models.

In both you explicity write the optimiser steps. Different optimisers will have
different optimiser state and this can get a bit annoying. See
https://jax.readthedocs.io/en/latest/jax.example_libraries.optimizers.html.

Optimizers are typically modelled as `(init_fun, update_fun, get_params)` where
`get_params` is very simple if you simply keep separate your model and optimzer
state.
You can look at optax but it feels like it is not worth the added dependency.
The examples in `jax/example_libraries/optimizers.py` might be better.
Also just generally look in `jax/examples`.

I think in general, you end up with a library of functions that look like this
for optimizers
```python
def train_step(grad_fun, params, opt_state, data):
    ...
```

# old

https://blog.evjang.com/2019/02/maml-jax.html

pip install --upgrade "jax[cuda]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

