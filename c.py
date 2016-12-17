from functools import wraps
import time
import inspect
import decorator
import logging
from pdb import set_trace
logging.getLogger().setLevel(logging.INFO)

_version = 0

try:
    _cache
except NameError as e:
    _cache = dict()

class VersionedCachedComputation():
    def __init__(self, fun, *args, **kwargs):
        # kwargs is somehow never populated, annoying.
        argspec = inspect.getfullargspec(fun)
        kwargs = dict()
        for i, v in enumerate(argspec.defaults[::-1]):
            k = argspec.args[-(i+1)] # the defaults are already in here
            kwargs[k] = v
        args = args[:-len(kwargs)]
        self._args = args
        self._versioned_args = kwargs.get('v_args', None)
        self._kwargs = kwargs
        if 'v_args' in kwargs:
            self._kwargs.pop('v_args')
        self._fun = fun
        self._name = '{}:{}'.format(inspect.getabsfile(fun), fun.__name__)
        # set_trace()

    def _get_key(self):
        """ function signature key """
        key = self._name, self._args, frozenset(self._kwargs.items())
        if self._versioned_args is not None:
            key += tuple([x._get_key() for x in self._versioned_args])
        return key

    def compute(self, force=False):
        global _cache
        key = self._get_key()
        if key in _cache:
            logging.info("retrieve from cache for {}".format(key))
            res = _cache[key]
        else:
            logging.info("compute for {}".format(key))
            if self._versioned_args is not None:
                v_args = [x.compute() for x in self._versioned_args]
                res = self._fun(*self._args, v_args=v_args, **self._kwargs)
            else:
                res = self._fun(*self._args, **self._kwargs)
            _cache[key] = res
        return res

@decorator.decorator(VersionedCachedComputation)
def A(x, y='here', z='more'):
    time.sleep(1)
    return str(x) + ":" + str(y)

@decorator.decorator(VersionedCachedComputation)
def B(x, y='more', v_args=[A(41.3, 23)]):
    time.sleep(1)
    return str(x) + ":" + str(y) + ':' + str(v_args[0])








# NOPE

# # using decorator.decorate allows you to avoid closures
# def _versioned_cached_computation_factory(fun, *args, **kwargs):
#     return VersionedCachedComputation(fun, *args, *kwargs)
#
# def versioned_cached_computation_factory(fun):
#     return decorator.decorate(fun, _return_vcc)
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

