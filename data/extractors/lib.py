import inspect
import logging
import tempfile
import shutil
import threading
import pyarrow as pa
import pyarrow.parquet as pq
import os
import sys

def say_my_name(depth=-1):
    frame = sys._getframe(depth)
    _locals = frame.f_back.f_locals
    filename = os.path.realpath(_locals['__file__'])
    myname =  os.path.basename(filename).replace('.py', '')
    mydir = os.path.dirname(filename)
    if myname == '__init__':
        myname = os.path.basename(mydir)
    assert '_extractor' in myname
    myname = myname.replace('_extractor', '')
    basedir = get_basedir(myname)
    datadir = os.path.join(basedir, 'data')
    metadatadir = os.path.join(basedir, 'metadata')
    # TODO: consider named tuple
    dirs = [mkdir_if_needed(x) for x in [mydir, myname, basedir, datadir, metadatadir]]
    return dirs

def get_basedir(extractor_name):
    return os.path.join(os.path.expanduser('~/projects/data/extractor={}'.format(extractor_name)))

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
    print('writing {}'.format(filename))
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_to_dataset(table, root_path=filename, partition_cols=partition_cols, preserve_index=preserve_index)


def try_convert_inplace(df):
    for k in df:
        try:
            df[k] = pd.to_datetime(df[k])
        except Exception as e:
            continue

def move_and_remove_nonblocking(path):
    tempdir = tempfile.mkdtemp()
    logging.warning("mv %s %s && rmdir %s &" % (path, tempdir, tempdir))
    shutil.move(path, tempdir)
    threading.Thread(target=shutil.rmtree, args=[tempdir]).start()

class DataPuller():
    """
    operate in overwrite mode for now
    """
    def __init__(self, name, get_and_write, get_filename):
        self._get_and_write = get_and_write
        self._get_filename = get_filename
    def get(self, *args, return_data=False, force=False, **kwargs):
        filename = self._get_filename(*args, **kwargs)
        if not os.path.exists(filename) or force:
            print('{} does not exist'.format(filename))
        else:
            print('{} exists. set force to True to repull'.format(filename_zip))
    def load(self, *args, **kwargs):
        """ ignore for now """
        pass


