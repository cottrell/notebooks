"""
Likely buggy. Just a sketch.
"""
import json
import logging
import os
import threading
import time
from collections import deque
from functools import wraps

import ratelimit
from joblib.memory import _build_func_identifier
from ratelimit import RateLimitException

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class RateLimitPersistMixin:
    def _write_state_to_fs(self):
        data = {k: getattr(self, k) for k in self.state_keys}
        logging.debug(f'writing {data} to {self.persist_filename}')
        with open(self.persist_filename, 'w') as fout:
            json.dump(data, fout)

    def _load_state_from_fs(self):
        if os.path.exists(self.persist_filename):
            data = json.load(open(self.persist_filename))
            logging.debug(f'read {data} from {self.persist_filename}')
            for k, v in data.items():
                assert k in self.state_keys, f'{k} not in {self.state_keys}'
                setattr(self, k, v)

    def _set_persist_func(self, func):
        # we need these levels to avoid clashing when chaining decorators
        level = getattr(func, '_ratelimit_persist_level', -1) + 1
        setattr(func, '_ratelimit_persist_level', level)
        if self.persist_base_dir is None:
            self.persist_dir = os.path.join(os.path.dirname(func.__code__.co_filename), 'ratelimit_state', f'{func.__name__}_{level}')
        else:
            self.persist_dir = os.path.join(self.persist_base_dir, _build_func_identifier(func))
        logging.debug(f'persist_dir={self.persist_dir}')
        os.makedirs(self.persist_dir, exist_ok=True)
        self.persist_filename = os.path.join(self.persist_dir, 'data.json')

    def clear_state(self):
        if os.path.exists(self.persist_filename):
            logging.debug(f'removing {self.persist_filename}')
            os.remove(self.persist_filename)
        self.reset_memory_state()

    @property
    def state(self):
        return {k: getattr(self, k) for k in self.state_keys}


class RateLimitDecorator(ratelimit.RateLimitDecorator, RateLimitPersistMixin):
    def __init__(self, *, persist_dir=None, **kwargs):
        self.persist_base_dir = persist_dir
        self.state_keys = ['last_reset', 'num_calls']
        super().__init__(**kwargs)

    def __call__(self, func):
        self._set_persist_func(func)
        func = super().__call__(func)
        self._load_state_from_fs()  # NOTE: this is kind of the actual "init"

        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            self._write_state_to_fs()
            return res

        wrapper.limiter = self
        return wrapper

    def reset_memory_state(self):
        self.last_reset = self.clock()
        self.num_calls = 0


limits = RateLimitDecorator


@limits(calls=4, period=100)
def _test():
    print('hello')

# chaining example
@limits(calls=4, period=3)
@limits(calls=104, period=30)
def _test3():
    print('hello')


class RateLimitDecoratorExact(RateLimitPersistMixin):
    def __init__(self, persist_dir=None, clock=time.monotonic, calls=15, period=900, raise_on_limit=True):
        self.persist_base_dir = persist_dir
        self.state_keys = ['calltimes']
        self.clock = clock
        self.raise_on_limit = raise_on_limit
        self.calls = calls
        self.period = period
        self._calltimes = deque([], maxlen=self.calls)
        self.lock = threading.RLock()

    def reset_memory_state(self):
        self._calltimes = deque([], maxlen=self.calls)

    # need property faff for json serialize
    @property
    def calltimes(self):
        return list(self._calltimes)

    @calltimes.setter
    def calltimes(self, value):
        self._calltimes = deque(value, maxlen=self.calls)

    def __period_remaining(self):
        if len(self.calltimes) < self.calls:
            return -99999
        elapsed = self.clock() - self.calltimes[0]
        return self.period - elapsed

    def __call__(self, func):
        self._set_persist_func(func)
        self._load_state_from_fs()  # NOTE: this is kind of the actual "init"

        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                period_remaining = self.__period_remaining()
                if period_remaining <= 0:
                    res = func(*args, **kwargs)
                    self._calltimes.append(self.clock())
                    self._write_state_to_fs()
                else:
                    if self.raise_on_limit:
                        raise RateLimitException(f'too many calls. period_remaining={period_remaining}', period_remaining)
                    return
            return res

        wrapper.limiter = self
        return wrapper


limits_exact = RateLimitDecoratorExact


@limits_exact(calls=4, period=3)
def _test2():
    print('hello')

