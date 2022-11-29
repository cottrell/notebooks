"""
see https://github.com/google/jax/discussions/7801

Example of how to create pytree for params to do sensitivities.
"""
import numpy as np
from jax.tree_util import tree_unflatten, tree_flatten, build_tree
import jax
import jax.numpy as jnp
import haiku as hk

class MyModule(hk.Module):

  def __init__(self, output_size, name=None):
    super().__init__(name=name)
    self.output_size = output_size

  def __call__(self, x):
    j, k = x.shape[-1], self.output_size
    w_init = hk.initializers.TruncatedNormal(1. / np.sqrt(j))
    w = hk.get_parameter("w", shape=[j, k], dtype=x.dtype, init=w_init)
    b = hk.get_parameter("b", shape=[k], dtype=x.dtype, init=jnp.ones)
    return jnp.dot(x, w) + b


def f_fn(x):
    a = MyModule(output_size=1)
    return a(x)

f = hk.without_apply_rng(hk.transform(f_fn))
x = np.random.randn(10, 2).astype(np.float32)
rng = jax.random.PRNGKey(0)
params = f.init(rng, x)
yp = f.apply(params, x)

# you can hack the leaves and re-assemble
# leaves, tree_def = tree_flatten(params)
# p0 = tree_unflatten(tree_def, leaves)

# or better to do this
p1 = {
  'my_module': {
    'w': jnp.array(np.random.randn(*params['my_module']['w'].shape)),
    'b': jnp.array(np.random.randn(*params['my_module']['b'].shape))
  }
}
p1 = hk.data_structures.to_immutable_dict(p1)

yp1 = f.apply(p1, x)
