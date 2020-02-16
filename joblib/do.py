from ratelimit import limits, sleep_and_retry
import superbasic
import joblib
import os
import pandas as pd
import numpy as np
import numpy.random as nr
from joblib import Memory
_mydir = os.path.dirname(__file__)
cachedir = os.path.join(_mydir, 'joblib_cache')
memory = Memory(cachedir, verbose=10, backend='superbasic')

A = nr.randn(100000, 50)
df = pd.DataFrame(A)


# @sleep_and_retry
# @limits(calls=1, period=_period_seconds)
# WARNING: persistant state here, clear if worried
_period_seconds = 1
@memory.cache
def f(x):
    print("more")
    print("here!")
    df = pd.DataFrame(np.random.randn(100, 5))
    df['category'] = 'something'
    return {'a': df , 'b': [1,2,3,], 'c': 'this is ok'}

def dumb(fun):
    def inner(*args, **kwargs):
        args = []


@memory.cache
def g(x, y):
    print('g')
    return x + y

# see do.f.call(1) and do.f.clear() for forcing/reseting etc

# stupid trick: you call counter.call() to force it, counter() is fixed otherwise
@memory.cache
def counter():
    if counter.check_call_in_cache():
        return counter() + 1
    else:
        return 0

if __name__ == '__main__':
    f(1)
    f(1)
    f(2)
