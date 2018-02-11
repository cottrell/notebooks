"""
Data is sparse with about 10% density.
"""
import pandas as pd
import zipfile
import bc
import numpy as np

def read_zip():
    d = dict()
    for filename in ['test', 'train']:
        f = filename + '.csv.zip'
        z = zipfile.ZipFile(f).open(filename + '.csv')
        df = pd.read_csv(z)
        print('{} {}'.format(f, df.shape))
        d[filename] = df
    return d

try:
    d
except NameError as e:
    d = read_zip()

train = d['train']

colbytypes = train.dtypes.reset_index()
colbytypes.columns = ['col', 'dtype']
colbytypes['dtype'] = colbytypes['dtype'].astype(str)
colbytypes = colbytypes.set_index('dtype').sort_index()['col']
icols = colbytypes['int64'].tolist()
fcols = colbytypes['float64'].tolist()

xcols = [x for x in train.columns if x not in ['ID', 'TARGET']]
ycol = 'TARGET'
