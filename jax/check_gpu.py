#!/usr/bin/env python
"""Check JAX GPU capability: basic ops, Cholesky (cuSOLVER), and vmap."""
import jax
import jax.numpy as jnp
from jax import random

key = random.PRNGKey(0)

# 1. Basic matmul (cuBLAS)
x = random.normal(key, (1000, 1000), dtype=jnp.float32)
y = jnp.dot(x, x.T).block_until_ready()
print(f"matmul : ok  device={y.devices()}")

# 2. Cholesky (cuSOLVER)
try:
    A = jnp.eye(64) + 0.1
    L = jax.scipy.linalg.cholesky(A, lower=True).block_until_ready()
    print(f"cholesky: ok  device={L.devices()}")
except Exception as e:
    print(f"cholesky: FAILED  ({e})")

# 3. vmap + cholesky (used in GPR training)
try:
    batch = jnp.stack([jnp.eye(32) + 0.1] * 16)
    Ls = jax.vmap(lambda a: jax.scipy.linalg.cholesky(a, lower=True))(batch).block_until_ready()
    print(f"vmap+cholesky: ok  device={Ls.devices()}")
except Exception as e:
    print(f"vmap+cholesky: FAILED  ({e})")

print(f"\nplatform: {jax.default_backend()}")
print(f"devices : {jax.devices()}")
