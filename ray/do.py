import numpy as np
import ray

def init():
    return ray.init()

def bounce():
    ray.disconnect()
    # might be incorrect
    return ray.init()


def f(x):
    return x ** 2

f_remote = ray.remote(f)

def g(x, seed=1):
    np.random.seed(seed)
    x = np.random.randn(10, 5) + x
    return x

g_remote = ray.remote(g)
