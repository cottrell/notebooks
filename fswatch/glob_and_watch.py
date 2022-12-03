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
    """ use this to test your glob pattern """
    # find is probably faster, whatever
    for x in _glob.iglob(os.path.join(dirname, '**/*'), recursive=True):
        yield [datetime.datetime.now().strftime(_date_format), os.path.abspath(x), ['glob']]

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
            x[2] = x[2].split(',')
            yield x

def glob_and_watch(dirname):
    """
    A full listing of the directory and all subsequent changes.
    Starts the watch first, then globs.

    $ ./glob_and_watch glob-and-watch ./tmp
        ['2018-07-25T22:57:36', '/path/to/somewhere/tmp/asdf', ['glob']]
        ['2018-07-25T22:57:36', '/path/to/somewhere/tmp/jadfs', ['glob']]
        ['2018-07-25T22:57:36', '/path/to/somewhere/tmp/jj', ['glob']]
        ['2018-07-25T22:57:36', '/path/to/somewhere/tmp/j', ['glob']]
        ['2018-07-25T21:57:48', '/path/to/somewhere/tmp/a', ['Created', 'IsFile']]
        ['2018-07-25T21:57:48', '/path/to/somewhere/tmp/b', ['Created', 'IsFile']]
        ['2018-07-25T21:57:52', '/path/to/somewhere/tmp/a', ['Created', 'PlatformSpecific', 'Updated', 'IsFile']]
        ['2018-07-25T21:57:55', '/path/to/somewhere/tmp/a', ['Created', 'PlatformSpecific', 'Updated', 'IsFile']]
        ['2018-07-25T21:57:56', '/path/to/somewhere/tmp/a', ['Created', 'Removed', 'PlatformSpecific', 'Updated', 'IsFile']]
        ['2018-07-25T21:57:56', '/path/to/somewhere/tmp/b', ['Created', 'Removed', 'IsFile']]
    """
    p_watch = watch(dirname)
    p_glob = glob(dirname)
    for x in itertools.chain(p_glob, p_watch):
        assert len(x) == 3, 'bad length {}'.format(x)
        yield x

def watch(dirname):
    """
    watches a directory for events
    """
    for x in Watch(dirname):
        yield x

if __name__ == "__main__":
    argh.dispatch_commands([glob, watch, glob_and_watch])
