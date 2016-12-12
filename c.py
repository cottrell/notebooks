"""
@CachableComputationFactory
def f(a, b=None):
    pass

f(1.2).compute()
f(1.2).compute(force=True)
"""
from functools import wraps
import inspect

class Counter():
    def __init__(self):
        self._current = 0
        self._min = 0
        self._max = 0
    def get(self):
        return self._current
    def __call__(self):
        return self._current
    def go(self, x):
        self._current = x

version = Counter()

class VersionedCachedComputation():
    def __init__(self, fun, *args, **kwargs):
        print('HEREHERE', kwargs)
        # TODO check argspec of fun and provided args, kwargs on init
        self._args = args
        self._versioned_args = kwargs.get('v_args', None)
        self._kwargs = kwargs
        if 'v_args' in kwargs:
            self._kwargs.pop('v_args')
        self._fun = fun
        self._name = fun.__name__
        print('{} versioned args: {}'.format(self._name, self._versioned_args))
    def compute(self):
        print("I am {} and I am running with args {}".format(self._name, (self._args, self._kwargs)))
        if self._versioned_args is not None:
            print("HERE")
            v_args = [x.compute() for x in self._versioned_args]
            return self._fun(*self._args, v_args=v_args, **self._kwargs)
        else:
            return self._fun(*self._args, **self._kwargs)
    def _get_args(self):
        args = self._args
        kwargs = self._kwargs
        if self._versioned_args is not None:
            kwargs['v_args'] = [x._get_args() for x in self._versioned_args]
        return args, tuple(kwargs.items())


class VersionedCachedComputationFactory(object):
    def __init__(self, name=None, **kwargs):
        self.name = name
        if self.name == None:
            self.name = 'unnamed' # how to get name from caller module
    def __call__(self, fun):
        # TODO need to get kwarg defaults ... wraps is not picking them  up
        print('{} computation construction from {}'.format(self.name, fun.__name__))
        @wraps(fun)
        def inner(*args, **kwargs):
            return VersionedCachedComputation(fun, *args, **kwargs)
        return inner


VCCF = VersionedCachedComputationFactory(name='main vccf')

@VCCF
def A(x, y=None):
    print("me I'm running x={}, y={}".format(x, y))
    return str(x) + ":" + str(y)

def b(x, y=None, v_args=[A(43.3, 23)]):
    print("me I'm running x={}, y={}".format(x, y))
    return str(x) + ":" + str(y) + ':' + str(v_args[0])

B = VCCF(b)

# these need to be the same
print(inspect.getfullargspec(b))
print(inspect.getfullargspec(B(12, 2).compute))


