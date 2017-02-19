import logging
import time
import pandas as pd
import threading
import contextlib


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
