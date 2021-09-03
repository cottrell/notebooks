import inspect
import hashlib
import os
import json

def memo_args(args, kwargs):
    return args, frozenset(kwargs.items())

def memo_func(fun):
    return fun.__class__.__qualname__, os.path.abspath(fun.__code__.co_filename), fun.__qualname__, inspect.getsource(fun) # fun.__code__.co_code


def myfunction(a=1, b=2):
    pass

def get_hash(key):
    return hashlib.sha1(json.dumps(key).encode()).hexdigest()

key = memo_func(myfunction)
hashed_key = get_hash(key)
print('key', key)
print('hashed_key', get_hash(key))


