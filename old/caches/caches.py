from functools import wraps
import time
import decorator
import logging
from pdb import set_trace
from dask.delayed import Delayed
from dask import delayed
import pickle
import hashlib

# key is good in dask now. the other stuff not yet

class Helper():
    def __init__(self, version, func, *args, **kwargs):
        self.version = version
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.delayed = delayed(pure=True)(func)(*args, **kwargs)
    @property
    def key(self):
        return (self.version, self.delayed.key)
    @property
    def hashkey(self):
        return hashlib.sha1(pickle.dumps((self.version, self.delayed.key))).hexdigest()
    def compute(self):
        self._value = self.delayed.compute()
        return self._value
    def write(self):
        pass
    def read(self):
        pass

def __versioned(func, *args, **kwargs):
    return Helper(func.version, func, *args, **kwargs)

def versioned(version=None):
    def _versioned(f):
        f.version = version
        return decorator.decorate(f, __versioned)
    return _versioned

@versioned(version=1)
def A(x, y='here', z='more'):
    print('COMPUTING')
    return str(x) + ":" + str(y)

@versioned(version=1)
def B(x, y='more', v_args=[A(41.3, 23)]):
    print('COMPUTING')
    return str(x) + ":" + str(y) + ':' + str(v_args[0])

# @delayed(pure=True)
# def C(x, y='more', v_args=[B(1111), A(41.3, 23)]):
#     print('COMPUTING')
#     return str(x) + ":" + str(y) + ':' + str(v_args[0])
