import inspect
import time
import concurrent
from contextlib import contextmanager
import glob
import pandas as pd
import functools
import logging
import tempfile
import shutil
import threading
import pyarrow as pa
import pyarrow.parquet as pq
import os
import sys
import datetime
from mylib import bok, wok
from mylib.tools import run_tasks_in_parallel

_timecol = 'ingress_time'
_basedir = os.path.expanduser('~/projects/data')
_trash = os.path.join(_basedir, 'trash')

date_format = '%Y-%m-%d'
date_ranges = {
        'default': {'start': '2010-01-01'}
        }

def get_basedir(extractor_name):
    return os.path.join(_basedir, extractor_name)

def extractor(**kwargs):
    def inner(fun):
        return StandardExtractorAppender(fun, **kwargs)
    return inner

def move_to_trash(filename_or_dirname):
    mkdir_if_needed(_trash)
    target = os.path.join(_trash,
            os.path.basename(filename_or_dirname) + '.' + datetime.datetime.now().isoformat())
    try:
        print('{} -> {}'.format(filename_or_dirname, target))
        shutil.move(filename_or_dirname, target)
    except Exception as e:
        print('no dir to clear {}'.format(filename_or_dirname))

def partition_enforcer(partition_cols):
    def inner(fun):
        def _inner(*args, **kwargs):
            for partition_dict, df in fun(*args, **kwargs):
                for k in partition_dict:
                    if k in df.columns:
                        raise Exception('{} found in partition_dict *and* df.columns! Not allowed.')
                pcols = [x for x in partition_cols if x not in partition_dict]
                if pcols:
                    g = df.groupby(pcols)
                    pdict = dict(partition_dict)
                    for k, v in g:
                        if not isinstance(k, tuple):
                            k = (k,)
                        pdict.update(dict(zip(pcols, k)))
                        v = v.drop(pcols, axis=1)
                        yield pdict, v
                else:
                    yield partition_dict, df
        return _inner
    return inner

@contextmanager
def dumblock(dirname):
    """ requires write access to location of dirname """
    lockdir = os.path.join(dirname, '_lock')
    locked = False
    attempts = 0
    sleepseconds = 1
    # TODO: test on kill, is not removing lockdir
    while not locked:
        try:
            os.makedirs(lockdir)
            locked = True
        except FileExistsError as e:
            print('{} exists. attempt {}. sleeping {}'.format(lockdir, attempts, sleepseconds))
            time.sleep(sleepseconds)
        except Exception as e:
            # only do this on other errors or success, not finally
            os.rmdir(lockdir)
            raise e
    yield
    os.rmdir(lockdir)

class StandardExtractorAppender():
    """
    Oriented around the DATA PULLING process and efficient updates/diff checks.
    Not how you would like it to be stored for later.

    fun: must be a generator function.

    Each call adds a timestamp col. Writes only new entries.

    Partitions can be given in the partition_dict or the df.

    You do not know the filename before running the function necessarily. This is now changed.

    This is not amazing. Pretty bad perf depending how the blocks come in. Have to load the entire
    bucket to check diffs. Could be smart with an index except THE WHOLE ROW is the index really.

    TODO: lock file clean up on kill
    TODO: incorporate schema see pdr
    """
    def __init__(self, fun, partition_cols=None, clearable=False):
        self.partition_cols = [] if partition_cols is None else partition_cols
        self.name = get_name(fun)
        self.fun = partition_enforcer(self.partition_cols)(fun)
        self.basedir = get_basedir(self.name)
        self.clearable = clearable
    def filename(self, partition_dict):
        p = ''
        if self.partition_cols:
            p = ['{}={}'.format(k, partition_dict[k]) for k in self.partition_cols]
            p = os.path.join(*p)
        return os.path.join(self.basedir, p)
    def clear(self):
        """ Move entire dir to trash. Dangerous. TODO """
        if self.clearable:
            move_to_trash(self.basedir)
        else:
            print('clear {} manually for now. Dangerous as is large and mistakes costly.'.format(self.basedir))
        return
    def call(self, *args, **kwargs):
        """ Call only gen fun directly. Enrich, categorize and group. No write """
        now = datetime.datetime.now() # not sure which time this should be
        for partition_dict, df in self.fun(*args, **kwargs):
            df[_timecol] = now
            convert_to_categorical_inplace(df)
            yield partition_dict, df
    def __call__(self, *args, **kwargs):
        """Call and write *new entries* to file.

        New entries are computed by diffing to existing.

        TODO: lockfile on filename

        this logic is pretty awful, probably a better way to do this with.
        """
        max_workers = 10
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        fut = list()
        total_rows = 0
        for partition_dict, df in self.call(*args, **kwargs):
            total_rows += df.shape[0]
            filename = self.filename(partition_dict)
            # maybe_update(filename, df)
            fut.append(executor.submit(maybe_update, filename, df))
            print('{} rows processed'.format(total_rows))
        res = [x.result() for x in fut]
        # TODO: agg the reports
        return res
    def load(self):
        filename = self.basedir
        print('read_parquet {}'.format(self.basedir))
        return pd.read_parquet(filename)

def maybe_update(filename, df):
    report = dict(changed=[], unchanged=[])
    if not os.path.exists(filename):
        mkdir_if_needed(filename)
    with dumblock(filename):
        if len(glob.glob(os.path.join(filename, '*.parquet'))) == 0:
            write_parquet(df, filename)
        else: # a file exists
            df_orig = pd.read_parquet(filename)
            # TODO: put df through write read cycle if worried
            cols = [x for x in df_orig.columns if x != _timecol]
            a = pd.util.hash_pandas_object(df_orig[cols], index=False)
            b = pd.util.hash_pandas_object(df[cols], index=False)
            hashes_in_both = set(b).intersection(set(a))
            if len(hashes_in_both) == 0:
                # all new, nothing to check unless read write is busted`
                print('{} (100%) new entries.'.format(df.shape[0]))
                write_parquet(df, filename)
            else:
                new_hashes_or_values = set(b) - set(a)
                # for hashes in both, check if values are actually the same
                # index is NOT used so can mess with it
                df_orig.index = a.values
                df.index = b.values
                # use == bc safer on case of nan etc
                new = df.loc[hashes_in_both][cols]
                old = df_orig.loc[hashes_in_both][cols]
                # nans are a pain
                same_hashes_different_values = ~(
                        (new ==  old) | (new.isnull() & old.isnull())
                        ).all(axis=1)
                same_hashes_different_values = set(same_hashes_different_values[same_hashes_different_values].index)
                myprint = lambda x: print('{}: {}'.format(x, filename))
                if same_hashes_different_values:
                    myprint('found same hashes but diff values. this is unusual.')
                    new_hashes_or_values.update(same_hashes_different_values)
                if new_hashes_or_values:
                    mask = df.index.isin(new_hashes_or_values)
                    myprint('{} out of {} new entries.'.format(mask.shape[0], df.shape[0]))
                    write_parquet(df.iloc[mask], filename)
                    report['changed'].append(filename)
                else:
                    myprint('no new entries. not appending anything')
                    report['unchanged'].append(filename)
            # print('ls -l {}'.format(filename))
            # os.system('ls -l {}'.format(filename))
    return report


import traceback
def get_name(fun, depth=-1):
    name = fun.__name__
    assert name.startswith('get_'), 'name must start with get_ got {}'.format(name)
    name = name[4:]
    # mod = fun.__module__.split('.')[1]
    mod = fun.__module__.replace('.', '/')
    return os.path.join(mod, name)

def say_my_name(depth=-1):
    frame = sys._getframe(depth)
    _locals = frame.f_back.f_locals
    filename = os.path.realpath(_locals['__file__'])
    myname =  os.path.basename(filename).replace('.py', '')
    mydir = os.path.dirname(filename)
    if myname == '__init__':
        myname = os.path.basename(mydir)
    return [mydir, myname]

def mkdir_if_needed(k):
    if not os.path.exists(k):
        print('mkdir {}'.format(k))
        os.makedirs(k)
    return k

def render_date_arg(start=None, end=None):
    """ None means defaults. """
    parse = lambda x: datetime.datetime.strptime(x, date_format).date()
    if end is None:
        end = datetime.date.today()
    elif isinstance(end, str):
        end = parse(end)
    if start is None:
        start = date_ranges['default']['start']
    if isinstance(start, str):
        if start == 'oneweek':
            end = datetime.date.today()
            start = end - datetime.timedelta(days=7)
        else:
            start = parse(start)
    return start, end

def write_parquet(df, filename, partition_cols=None, preserve_index=False):
    """ write parquet dataset. *appends* to existing data. """
    print('writing df.shape = {} to {}'.format(df.shape, filename))
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_to_dataset(table, root_path=filename, partition_cols=partition_cols, preserve_index=preserve_index)


def move_and_remove_nonblocking(path):
    tempdir = tempfile.mkdtemp()
    logging.warning("mv %s %s && rmdir %s &" % (path, tempdir, tempdir))
    shutil.move(path, tempdir)
    threading.Thread(target=shutil.rmtree, args=[tempdir]).start()

def convert_to_categorical_inplace(df, thresh_hold=1000, na_value='None'):
    for k in df:
        if df[k].dtype.name in ('object', 'str'):
            df[k] = df[k].fillna('None')
            if df[k].nunique() < thresh_hold:
                df[k] = df[k].astype('category')

def try_convert_inplace(df):
    for k in df:
        try:
            df[k] = pd.to_datetime(df[k])
        except Exception as e:
            continue

