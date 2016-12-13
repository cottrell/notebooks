from functools import wraps
import inspect
import decorator
import logging
logging.getLogger().setLevel(logging.INFO)

class VersionedCachedComputation():
    def __init__(self, fun, *args, **kwargs):
        self._args = args
        self._versioned_args = kwargs.get('v_args', None)
        self._kwargs = kwargs
        if 'v_args' in kwargs:
            self._kwargs.pop('v_args')
        self._fun = fun
    def compute(self):
        logging.info("VCC args={}, kwargs={}".format(self._args, self._kwargs))
        if self._versioned_args is not None:
            v_args = [x.compute() for x in self._versioned_args]
            return self._fun(*self._args, v_args=v_args, **self._kwargs)
        else:
            return self._fun(*self._args, **self._kwargs)

# using decorator.decorate allows you to avoid closures
def _versioned_cached_computation_factory(fun, *args, **kwargs):
    return VersionedCachedComputation(fun, *args, *kwargs)

def versioned_cached_computation_factory(fun):
    return decorator.decorate(fun, _return_vcc)

@versioned_cached_computation_factory
def f(x, y='here'):
    print("me I'm running x={}, y={}".format(x, y))
    return str(x) + ":" + str(y)

@versioned_cached_computation_factory
def A(x, y='here'):
    print("me I'm running x={}, y={}".format(x, y))
    return str(x) + ":" + str(y)

@versioned_cached_computation_factory
def B(x, y='more', v_args=[A(43.3, 23)]):
    print("me I'm running x={}, y={}, v_args={}".format(x, y, v_args))
    return str(x) + ":" + str(y) + ':' + str(v_args[0])

# NOPE

# class VersionedCachedComputationFactory(object):
#     def __init__(self, fun, *args, **kwargs):
#         self._fun = fun
#         self._name = 'needname'
#         argspec = inspect.getfullargspec(fun)
#         self._kwarg_defaults = dict(zip(argspec.args[::-1], argspec.defaults[::-1]))
#         logging.info("VCCF.__init__:{} _kwarg_defaults={}".format(self._name, self._kwarg_defaults))
#     def __call__(self, *args, **kwargs):
#         kwargs_out = dict(self._kwarg_defaults)
#         kwargs_out.update(kwargs)
#         logging.info("VCCF.__call__:{} args={}, kwargs={}".format(self._name, args, kwargs_out))
#         return VersionedCachedComputation(self._fun, *args, **kwargs_out)
