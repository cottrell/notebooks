from functools import wraps

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

class CachableComputation():
    def __init__(self, fun, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._fun = fun
    def compute(self):
        return self._fun(*self._args, **self._kwargs)


class CachableFunction(object):
    def __init__(self, *args, **kwargs):
        pass
    def __call__(self, fun):
        @wraps(fun)
        def inner(*args, **kwargs):
            return CachableComputation(fun, *args, **kwargs)
        return inner


@CachableFunction()
def fun(x, y=None):
    print("me I'm running x={}, y={}".format(x, y))
