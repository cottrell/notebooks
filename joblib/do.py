from joblib import Memory
import os
import pandas as pd
import numpy as np
import numpy.random as nr
_mydir = os.path.dirname(__file__)
cachedir = os.path.join(_mydir, 'joblib_cache')
memory = Memory(cachedir, verbose=0)

A = nr.randn(100000, 50)
df = pd.DataFrame(A)

@memory.cache
def f(x):
    print("more")
    print("here!")
    return x
