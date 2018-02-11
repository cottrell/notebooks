"""
persistent lightly abstracted version of
https://github.com/dask/cachey/blob/master/cachey/cache.py
"""
import simplekv

# TODO use to/from_dict_of_things. replace carrays with feather etc
def get_store(basename):
    from simplekv.fs import FilesystemStore
    return FilesystemStore(basename)

def _try_hash_result(result):
    try:
        hash(result)
    except TypeError:
        result = tuple(map(id, args)), str(kwargs)
    return result

def memo_key(args, kwargs):
    result = (args, frozenset(kwargs.items()))
    return _try_hash_result(result)

def memo_func(fun):
    # not terribly safe
    result = (fun.__code__.co_filename, fun.__name__, fun.__class__.__name__)
    return _try_hash_result(result)


