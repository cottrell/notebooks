import os
import glob
import datetime
import pickle
import sys
import inspect
import hashlib
from .tools import run_command_get_output, tempfile_then_atomic_move

# TODO copy stuff from git/libcache.py

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

# see data/kaggle/

class SimpleNode():
    """
    I have written something like this so many times it is not funny. Put something here and keep it simple to reuse.
    """
    def __init__(self, fun):
        self.fun = fun
        filename = os.path.abspath(fun.__code__.co_filename)
        self.dirname = os.path.join(os.path.basename(filename).replace('.py', ''), fun.__qualname__)
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
    def force_run(self, *args, **kwargs):
        obj = self.fun(*args, **kwargs)
        self._pickle_dated_file(obj)
    def get_latest(self):
        return pickle.load(open(self._get_latest_pickle(), 'rb'))
    def _get_dated_file(self, ext='.pickle'):
        return os.path.join(self.dirname, datetime.datetime.today().isoformat() + '.pickle')
    def _get_latest_pickle(self):
        files = glob.glob(os.path.join(self.dirname, '*.pickle'))
        if len(files) == 0:
            raise Exception("no files in {}".format(self.dirname))
        return files[-1]
    def _pickle_dated_file(self, obj):
        filename = self._get_dated_file(self.dirname)
        print('writing {}'.format(filename))
        pickle.dump(obj, open(filename, 'wb'))
    def __call__(self, *args, **kwargs):
        self.force_run(*args, **kwargs)
        return self.get_latest()


if __name__ == '__main__':
    # just trying to make sure the memo does not depend on the run path
    if len(sys.argv) > 1:
        test_number = sys.argv[1]
        __test()
    else:
        _test()
