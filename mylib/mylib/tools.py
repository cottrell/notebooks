import logging
import concurrent.futures
import subprocess
import time
import pandas as pd
import threading
import contextlib
import asyncio
import collections

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

def convert_to_categorical_inplace(df):
    for k in df:
        if df[k].dtype.name in ('object', 'str'):
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
    return v

def reorder_schema(schema, names):
    schema_names = [x.name for x in schema]
    index = dict(zip(schema_names, range(len(schema_names))))
    new_schema = [schema[index[x]] for x in names]
    from pyspark.sql.types import StructType
    return StructType(new_schema)

def df_to_pasteable_spark_schema(df):
    return schema_tuples_to_pasteable_spark_schema(df_to_schema_tuples(df))

def df_to_spark_schema(df):
    return schema_tuples_to_spark_schema(df_to_schema_tuples(df))

def schema_tuples_to_pasteable_spark_schema(d, print_string=True):
    import pyspark.sql.types as t
    # convoluted but using actual objects as test
    s = list()
    for k, v in d:
        if v.startswith('int'):
            temp = k, t.IntegerType()
        elif v.startswith('object') or v.startswith('str'):
            temp = k, t.StringType()
        elif v.startswith('float'):
            temp = k, t.DoubleType()
        elif v.startswith('date'):
            temp = k, t.DateType()
        else:
            raise Exception('uh oh {} {}'.format(k, v))
        temp = 't.StructField("{}", t.{}())'.format(temp[0], temp[1])
        s.append(temp)
    s = '\n    ' + ',\n    '.join(s)
    s = "import pyspark.sql.types as t\nschema = t.StructType([{}\n    ])".format(s)
    if print_string:
        print(s)
    else:
        return s

def schema_tuples_to_spark_schema(d):
    import pyspark.sql.types as t
    s = list()
    for k, v in d:
        if v.startswith('int'):
            temp = k, t.IntegerType()
        elif v.startswith('object') or v.startswith('str'):
            temp = k, t.StringType()
        elif v.startswith('float'):
            temp = k, t.DoubleType()
        elif v.startswith('date'):
            temp = k, t.DateType()
        else:
            raise Exception('uh oh {} {}'.format(k, v))
        s.append(t.StructField(*temp))
    return t.StructType(s)

def dict_to_spark_schema(d):
    """ use tuples instead. spark schema are ordered so be careful """
    raise Exception('use schema_tuples_to_spark_schema')

def df_to_schema_tuples(df):
    return list(df.dtypes.map(lambda x: x.name).items())

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

def run_tasks_in_parallel(*tasks, max_workers=10, wait=True):
    # http://masnun.rocks/2016/10/06/async-python-the-different-forms-of-concurrency/
    # https://www.reddit.com/r/learnpython/comments/72a8ek/why_bother_using_asyncio_when/
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    fut = [executor.submit(task) for task in tasks]
    # executor.shutdown(wait=wait) # apparently just returning .result triggers the wait. probably the context manager.
    if wait:
        return [x.result() for x in fut]
    else:
        return fut


@contextlib.contextmanager
def spark_manager(spark_master=None, name='default name'):
    if spark_master is None:
        spark_master = os.environ['SPARK_MASTER']
    conf = SparkConf().setMaster(spark_master) \
                      .setAppName(name) \
                      .set("spark.executor.memory", '1000m')
    spark_context = SparkContext(conf=conf)
    try:
        yield spark_context
    finally:
        spark_context.stop()

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

