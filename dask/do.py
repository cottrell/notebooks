import dask.delayed
import dask.cache

_cache = dask.cache.Cache(1e9)
_cache.register()

@dask.delayed(pure=True)
def f(x, y=1):
    print('compute f {}'.format((x, y)))
    return x, y

@dask.delayed(pure=True)
def ff(x, y=1):
    print('compute ff {}'.format((x, y)))
    return x, y

@dask.delayed(pure=True)
def g(x, z, y=1):
    z(x)
    z(x)
    z(x)
    print('compute b {}'.format((x, y, z)))
    return x, y, z(x)

@dask.delayed(pure=True)
def g2(x, z, y=1):
    print('compute g2 {}'.format((x, y, z)))
    return x, y, z

@dask.delayed(pure=True)
def g3(x, z, y=1):
    print('compute g2 {}'.format((x, y, z)))
    return x, y, z

def factory(x, z, y=1):
    return g2(x, f(x), y=y)

a = f(1)
b = g(1, f)
c = g2(1, f(1), y=ff(2))
a.visualize('a.png')
b.visualize('b.png')
c.visualize('c.png')
f.visualize('f.png')
g.visualize('g.png')
g2.visualize('g2.png')
