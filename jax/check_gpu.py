#!/usr/bin/env python
def check_gpu():
    from jax.extend.backend import get_backend
    import jax.numpy as jnp
    from jax import random
    key = random.PRNGKey(0)

    size = 3000
    x = random.normal(key, (size, size), dtype=jnp.float32)
    jnp.dot(x, x.T).block_until_ready()  # runs on the GPU

    return get_backend().platform


if __name__ == '__main__':
    print(check_gpu())
