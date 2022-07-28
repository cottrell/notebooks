"""
A reminder of rough setup.

1. define the build_forward_fn. I think you only need to inherit from hk.Module if you want to define some new kind of block (not 100% sure yet)
2. you can partition the parameters into differentiable/not-differentiable later in the loss function
3. create the loss function, use the merge to combine parameters if needed.

See https://github.com/deepmind/dm-haiku/blob/main/examples/transformer/train.py

https://theaisummer.com/jax-transformer/

I think can use my usual vanilla training loop for now.

Training subset of params
https://dm-haiku.readthedocs.io/en/latest/notebooks/non_trainable.html
"""

# I think this is the standard flow

def build_forward_fn(**static_params):
    def forward_fn(data, is_training=True):
        pass
    return forward_fn(data)


def lm_loss_function(forward_fn, params, rng, data, is_training=True):
    # something like this that you will partial away
    pass


def train_step(params, momentums, scales, x, y, x_test=None, y_test=None, *, lr):
    # something like this (as I would do in vanilla jax)
    # grads = grad_fun(params, x, y, x_test, y_test)
    loss_value, grads = grad_fun(params, x, y, x_test=x_test) # , y_test=y_test)
    beta = 0.1
    momentums = tree_map(lambda m, g: (1 - beta) * m + beta * g, momentums, grads)
    scales = tree_map(lambda s, g: (1 - beta) * s + beta * g ** 2, scales, grads)
    params = tree_map(lambda p, m, s: p - lr * m / jnp.sqrt(s + 1e-5), params, momentums, scales)
    return params, momentums, scales, loss_value