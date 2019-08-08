import ray

def init():
    ray.init()

def f(x):
    print('here', x)
    return x ** 2

f_remote = ray.remote(f)

def g(x):
    print('here', x)
    return x + 2

g_remote = ray.remote(g)
