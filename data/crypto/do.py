import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import glob
import inspect

def get_pandas_read_csv_defaults():
    # probably fragile
    i = inspect.getfullargspec(pd.read_csv)
    v = i.defaults
    k = i.args[-len(v):]
    kwargs = dict(zip(k, v))
    return kwargs

_mydir = os.path.dirname(os.path.realpath('__file__'))

kwargs = get_pandas_read_csv_defaults()
kwargs['thousands'] = ',' # always do this
# kwargs['parse_dates'] = ['Date']
kwargs['na_values'] = ['-']
kwargs['dtype'] = 'str'
dtype = {
 'Close': 'float',
 'High': 'float',
 'Low': 'float',
 'Market Cap': 'float',
 'Open': 'float',
 'Volume': 'float'
 }

meta = pd.read_csv(os.path.join(_mydir, 'Top100Cryptos/data/100 List.csv'))
names = meta.Name.tolist()
files = [os.path.join(_mydir, 'Top100Cryptos/data/{}.csv'.format(x)) for x in names]
# files = glob.glob(os.path.join(_mydir, 'Top100Cryptos/data/*.csv'))
dfs = list()
datadir = os.path.join(_mydir, 'parsed')
if not os.path.exists(datadir):
    os.makedirs(datadir)
for i, (name, f) in enumerate(zip(names, files)):
    mtime = os.path.getmtime(f)
    dirname = os.path.join(datadir, 'name={}/mtime={}'.format(name, mtime))
    filename = os.path.join(dirname, 'data.parquet')
    if not os.path.exists(filename):
        df = pd.read_csv(f, **kwargs)
        df = pa.Table.from_pandas(df)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        print('writing {}'.format(filename))
        pq.write_table(df, filename)
    pq.read_table('./parsed')
