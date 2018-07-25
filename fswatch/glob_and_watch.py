#!/usr/bin/env python
import datetime
import subprocess
import shlex
import argh
import glob as _glob
import os
import logging
import itertools
logging.getLogger().setLevel(logging.INFO)

_date_format = '%Y-%m-%dT%H:%M:%S'

def glob(dirname):
    # find is probably faster, whatever
    for x in _glob.iglob(os.path.join(dirname, '**/*'), recursive=True):
        yield [datetime.datetime.now().strftime(_date_format), x, 'glob']

class Watch():
    def __init__(self, dirname):
        cmd = 'fswatch -Lrtux --format-time {} --event-flag-separator=, --latency=0.1 {}'.format(_date_format, dirname)
        cmd = shlex.split(cmd)
        logging.info('running {}'.format(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = p.returncode
        if status not in {0, None}:
            raise Exception('error: {} {} {}'.format(status))
        self.p = p
    def __iter__(self):
        for x in self.p.stdout:
            x = x.decode().split()
            assert len(x) == 3, 'bad length {}'.format(x)
            x[2] = x[2].split(',')
            yield x

def glob_and_watch(dirname):
    p_watch = watch(dirname)
    p_glob = glob(dirname)
    for x in itertools.chain(p_glob, p_watch):
        yield x

def watch(dirname):
    for x in Watch(dirname):
        yield x

if __name__ == "__main__":
    argh.dispatch_commands([glob, watch, glob_and_watch])
