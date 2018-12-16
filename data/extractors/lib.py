import inspect
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

_timecol = 'ingress_time'
_basedir = os.path.expanduser('~/projects/data')
_trash = os.path.join(_basedir, 'trash')

def get_basedir(extractor_name):
    return os.path.join(_basedir, extractor_name)

def extractor(**kwargs):
    def inner(fun):
        return StandardExtractorAppender(fun, **kwargs)
    return inner

def standard_filename_generator(*args, **kwargs):
    # might need tuple ordering: TODO
    if kwargs:
        raise Exception('nip')
    return ''

class StandardExtractorAppender():
    """
    Single file! Use partitioning if you need to split it do not add complicated accessors for load.

    No partitioning for now.

    Each call adds a timestamp col. Writes only new entries.
    """
    def __init__(self, fun, filename=None, arg_gen=None):
        self.name = get_name(fun)
        self.fun = fun
        self.basedir = get_basedir(self.name)
        # actually a dirname
        self._filename_generator = standard_filename_generator if filename is None else filename
        self.arg_gen = arg_gen # for examples, nip
    def filename(self, *args, **kwargs):
        return os.path.join(self.basedir, self._filename_generator(*args, **kwargs))
    def clear(self):
        """ Move entire dir to trash. Dangerous. TODO """
        mkdir_if_needed(_trash)
        target = os.path.join(_trash,
                os.path.basename(self.basedir) + datetime.datetime.now().isoformat())
        try:
            print('{} -> {}'.format(self.basedir, target))
            shutil.move(self.basedir, target)
        except Exception as e:
            print('no dir to clear {}'.format(self.basedir))
    def load(self):
        return pd.read_parquet(self.basedir)
    def call(self, *args, **kwargs):
        """ Call only. No write """
        now = datetime.datetime.now()
        df = self.fun(*args, **kwargs)
        df[_timecol] = now
        convert_to_categorical_inplace(df)
        return df
    def __call__(self, *args, **kwargs):
        """ call and write *new entries* to file.

        New entries are computed by diffing to existin.
        """
        df = self.call(*args, **kwargs)
        filename = self.filename(*args, **kwargs)
        if not os.path.exists(filename):
            mkdir_if_needed(filename)
        if len(glob.glob(os.path.join(filename, '*.parquet'))) == 0:
            write_parquet(df, filename)
        else: # a file exists
            df_orig = pd.read_parquet(filename)
            # TODO: put df through write read cycle if worried
            cols = [x for x in df_orig.columns if x != _timecol]
            a = pd.util.hash_pandas_object(df_orig[cols], index=False)
            b = pd.util.hash_pandas_object(df[cols], index=False)
            same = set(b).intersection(set(a))
            if len(same) == 0:
                # all new, nothing to check unless read write is busted`
                print('{} new entries.'.format(len(df.shape[0])))
                write_parquet(df, filename)
            else:
                # are sames actually same?
                # index is NOT used so can mess with it
                df_orig.index = a.values
                df.index = b.values
                same = list(same) # not sure if needed
                # use == bc safer on case of nan etc
                same_but_diff = ~(df.loc[same][cols] == df.loc[same][cols]).all(axis=1)
                mask = same_but_diff.values
                if any(same_but_diff):
                    print('found same but diff. this is unusual.')
                    different = ~df.index.isin(same)
                    mask = mask | different
                if mask.any():
                    write_parquet(df.iloc[mask], filename)
                else:
                    print('no new entries. not appending anything')
        print('ls -l {}'.format(filename))
        os.system('ls -l {}'.format(filename))


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
    # assert '_extractor' in myname
    # myname = myname.replace('_extractor', '')
    basedir = get_basedir(myname)
    datadir = os.path.join(basedir, 'data')
    metadatadir = os.path.join(basedir, 'metadata')
    # TODO: consider named tuple
    dirs = [mkdir_if_needed(x) for x in [mydir, myname, basedir, datadir, metadatadir]]
    return dirs

def mkdir_if_needed(k):
    if not os.path.exists(k):
        print('mkdir {}'.format(k))
        os.makedirs(k)
    return k

date_format = '%Y-%m-%d'
date_ranges = {
        'bulk': {'start': '2010-01-01', 'end': '2018-12-09'}
        }

def render_date_arg(start, end=None):
    """
    start = 'bulk' to use hard coded bulk range.
    """
    parse = lambda x: datetime.datetime.strptime(x, date_format).date()
    if end in date_ranges:
        start = parse(date_ranges[start]['start'])
        end = parse(date_ranges[start]['end'])
    else:
        if isinstance(end, str):
            end = parse(end)
        if start is None:
            start = end - datetime.timedelta(days=1)
        elif isinstance(start, str):
            start = parse(start)
    return start, end

def write_parquet(df, filename, partition_cols=None, preserve_index=False):
    """ write parquet dataset. *appends* to existing data. """
    print('writing to {}'.format(filename))
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

