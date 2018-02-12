import os
import sys
import inspect
import hashlib
import simplekv
import decorator
from tools import run_command_get_output

def get_store(basename):
    from simplekv.fs import FilesystemStore
    return FilesystemStore(basename)

def memo_args(args, kwargs):
    return args, frozenset(kwargs.items())

def memo_func(fun):
    return fun.__class__.__qualname__, os.path.abspath(fun.__code__.co_filename), fun.__qualname__, inspect.getsource(fun) # fun.__code__.co_code

def _test_function():
    pass

class _TestClass():
    def _test_function(self):
        pass

def _test():
    # sanity
    a = run_command_get_output('python {} 1'.format(os.path.abspath(__file__)))
    b = run_command_get_output('cd && python {} 1'.format(os.path.abspath(__file__)))
    assert a['status'] == b['status'] == 0
    assert len(a['out']) != 0
    assert a['out'][0] != a['out'][1]
    assert b['out'][0] != b['out'][1]
    assert a['out'][0] == b['out'][0]
    assert a['out'][1] == b['out'][1]
    print('test pass')

def __test():
    tc = _TestClass()
    a = memo_func(_test_function)
    b = memo_func(tc._test_function)
    print(a)
    print(b)

if __name__ == '__main__':
    # just trying to make sure the memo does not depend on the run path
    if len(sys.argv) > 1:
        test_number = sys.argv[1]
        __test()
    else:
        _test()
