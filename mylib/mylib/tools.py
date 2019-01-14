import logging
import functools
import concurrent.futures
import subprocess
import time
import pandas as pd
import threading
import contextlib
import asyncio
import collections
import os
import tempfile

@contextlib.contextmanager
def tempfile_then_atomic_move(filename, dir=None, prefix='.tmp_'):
    if dir is None:
        dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.makedirs(dir)
    temp = tempfile.mktemp(prefix=prefix, dir=dir)
    yield temp
    print('atomic {} -> {}'.format(temp, filename))
    os.rename(temp, filename)

# https://fredrikaverpil.github.io/2017/06/20/async-and-await-with-subprocesses/
# https://docs.python.org/3/library/asyncio-subprocess.html

def run_command_get_output(cmd, shell=True, splitlines=True):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = p.communicate()
    status = p.returncode
    out = out.decode()
    err = err.decode()
    if splitlines:
        out = out.split('\n')
        err = err.split('\n')
    return dict(out=out, err=err, status=status)

def convert_nan_to_none_inplace(df, na_value='None'):
    for k in df:
        if df[k].dtype.name in ('object', 'str'):
            df[k] = df[k].fillna('None')

def convert_to_categorical_inplace(df, thresh_hold=1000, na_value='None'):
    for k in df:
        if df[k].dtype.name in ('object', 'str'):
            df[k] = df[k].fillna('None')
            if df[k].nunique() < thresh_hold:
                df[k] = df[k].astype('category')

def dict_of_lists_to_dict(d):
    r = dict()
    for k, v in d.items():
        for x in v:
            assert x not in r, 'clash {}'.format(x)
            r[x] = k
    return r

def list_of_tuples_to_dict_of_lists(d):
    out = collections.defaultdict(list)
    for k, v in d:
        out[k].append(v)
    return dict(out)

def invert_dict(d):
    r = dict()
    for k, v in d.items():
        if v not in r:
            r[v] = list()
        r[v].append(k)
    r = {k: sorted(v) for k, v in r.items()}
    return r

def df_to_schema_tuples(df):
    return list(df.dtypes.map(lambda x: x.name).items())

def apply_schema_to_df_inplace(df, schema):
    for k in df.columns:
        if df[k].dtype.name != schema[k]:
            df[k] = df[k].astype(schema[k])

def schedule_coroutine(target, *, loop=None):
    """Schedules target coroutine in the given event loop

    If not given, *loop* defaults to the current thread's event loop

    Returns the scheduled task.
    """
    if asyncio.iscoroutine(target):
        return asyncio.ensure_future(target, loop=loop)
    raise TypeError("target must be a coroutine, not {!r}".format(type(target)))

def run_in_background(non_co_callable, loop=None, executor=None):
    # not concellable
    if loop is None:
        loop = asyncio.get_event_loop()
    if callable(non_co_callable):
        return loop.run_in_executor(executor, non_co_callable)
    raise TypeError("target must be a callable, not {!r}".format(type(target)))

def run_in_foreground(*tasks, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(task, loop=loop) for task in tasks]
    tasks = asyncio.gather(*tasks)
    try:
        res = loop.run_until_complete(tasks)
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt: cancelling tasks ...")
        tasks.cancel()
        loop.run_forever()
        tasks.exception()

def _wrapped_errors(task):
    @functools.wraps(task)
    def inner():
        exception = None
        result = None
        try:
            result = task()
        except Exception as e:
            exception = e
        return dict(exception=exception, result=result)
    return inner

def test_wrapped_errors():
    def f():
        asdf
        return 'nothing'
    f = _wrapped_errors(f)
    return f()

def run_tasks_in_parallel(*tasks, max_workers=10, wait=True, raise_exceptions=False):
    """ WARNING: raise_exceptions changes the return structure. maybe this is obvious """
    # http://masnun.rocks/2016/10/06/async-python-the-different-forms-of-concurrency/
    # https://www.reddit.com/r/learnpython/comments/72a8ek/why_bother_using_asyncio_when/
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    if not raise_exceptions:
        tasks = map(_wrapped_errors, tasks)
    fut = [executor.submit(task) for task in tasks]
    # executor.shutdown(wait=wait) # apparently just returning .result triggers the wait. probably the context manager.
    if wait:
        return [x.result() for x in fut]
    else:
        return fut


class TimeLogger():

    def __init__(self, log=logging.warning):
        self.d = dict()
        self.log = log

    @contextlib.contextmanager
    def timedlogger(self, *name):
        start = time.time()
        # self.log("%s ..." % (name,))
        yield
        end = time.time()
        interval = end - start
        self.log("%f s : %s " % (interval, '-'.join(name)))
        self.d[name] = [start, end, interval]

    def get_frame(self):
        return pd.DataFrame(self.d, index=['start', 'stop', 'ellapsed']).T

    def clear(self):
        self.d = dict()

class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def hashed_pandas_apply(s, fun):
    u = s.unique()
    v = [fun(x) for x in u]
    return s.map(dict(zip(u, v)))
