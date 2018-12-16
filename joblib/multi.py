from ratelimit import limits, sleep_and_retry
from joblib import Memory
import superbasic
import joblib
import os
import pandas as pd
import numpy as np
import numpy.random as nr
_mydir = os.path.dirname(__file__)
location = os.path.join(_mydir, 'joblib_cache')
readonly_locations = [os.path.join(_mydir, 'joblib_cache{}'.format(i)) for i in range(3)]

A = nr.randn(100000, 50)
df = pd.DataFrame(A)

memory = superbasic.SingleWriteMultiReadMemory(location, readonly_locations=readonly_locations)
# memory = Memory(location, verbose=10, backend='superbasic', backend_options=dict(readonly_locations=readonly_locations))

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
