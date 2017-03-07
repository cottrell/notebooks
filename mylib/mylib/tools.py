import logging
import time
import pandas as pd
import threading
import contextlib
import asyncio

def dict_of_lists_to_dict(d):
    r = dict()
    for k, v in d.items():
        for x in v:
            assert x not in r, 'clash {}'.format(x)
            r[x] = k
    return r

def dict_to_spark_schema(d):
    import pyspark.sql.types as t
    s = list()
    r = dict(str=t.StringType(),
            float=t.DoubleType()) # etc
    for k, v in d.items():
        s.append(t.StructField(k, r[v]))
    return t.StructType(s)

def invert_dict(d):
    r = dict()
    for k, v in d.items():
        if v not in r:
            r[v] = list()
        r[v].append(k)
    r = {k: sorted(v) for k, v in r.items()}
    return v

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
    """Runs event loop in current thread until the given task completes

    Returns the result of the task.
    For more complex conditions, combine with asyncio.wait()
    To include a timeout, combine with asyncio.wait_for()
    """
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
    # finally:
    #     loop.close()


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
