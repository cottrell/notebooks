from ratelimit import limits, sleep_and_retry
from joblib import Memory
import os
import pandas as pd
import numpy as np
import numpy.random as nr
_mydir = os.path.dirname(__file__)
cachedir = os.path.join(_mydir, 'joblib_cache')

A = nr.randn(100000, 50)
df = pd.DataFrame(A)

memory = Memory(cachedir, verbose=1)

# @sleep_and_retry
# @limits(calls=1, period=_period_seconds)
# WARNING: persistant state here, clear if worried
_period_seconds = 1
@memory.cache
def f(x):
    print("more")
    print("here!")
    df = pd.DataFrame(np.random.randn(1000000, 5))
    df['category'] = 'something'
    return df

# see do.f.call(1) and do.f.clear() for forcing/reseting etc
