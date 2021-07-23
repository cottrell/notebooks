#!/usr/bin/env python
def check_gpu():
    from jax.lib import xla_bridge

    return xla_bridge.get_backend().platform


if __name__ == '__main__':
    print(check_gpu())
