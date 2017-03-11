import string
import os
import shutil
import numpy as np
import pandas as pd
from collections import defaultdict
import json
import bcolz
import logging

from pandas.core.internals import *

def _make_example():
    n = 1000000
    df = pd.DataFrame({'x': np.random.randint(0, 10000, size=n, dtype='i4'), 'y': np.random.random(n), 't': np.random.choice(list(string.ascii_lowercase), size=n), 'yy': np.random.random(n), 'tt':
        np.random.choice(list(string.ascii_lowercase[:10]), size=n)})
    df['yy'] = df['y'].values
    df['t'] = df['t'].astype('category')
    df['tt'] = df['tt'].astype('category')
    return df

df = _make_example()

def df_from_breakdown(d):
    blocks = d['blocks']
    df = list()
    for k in blocks:
        if k[0] == 'category':
            codes = blocks[k]['codes']
            categories = blocks[k]['categories']
            for i, placement in enumerate(blocks[k]['placement']):
                values = pd.Categorical.from_codes(codes[:,i], categories[i])
                values = make_block(values, [placement])
                df.append(values)
        else:
            values = make_block(blocks[k]['values'], blocks[k]['placement'])
            df.append(values)
    return tuple(df)

def breakdown(df):
    # TODO index
    df = df.consolidate()
    m = df.shape[0]
    d = dict()
    names = [_get_name(x) for x in df._data.blocks]
    names_counts = pd.Series(names).value_counts()
    cat_counter = defaultdict(int)
    for name, block in zip(names, df._data.blocks):
        placement = block.mgr_locs.as_array.tolist()
        if name[0] == 'category':
            assert len(placement) == 1, 'placement not length 1 {}'.format(placement)
            placement = placement[0]
            if name not in d:
                assert cat_counter[name] == 0
                d[name] = dict()
                d[name]['codes'] = np.empty((m, names_counts[name]), dtype=block.values.codes.dtype)
                d[name]['categories'] = list()
                d[name]['placement'] = list()
            d[name]['codes'][:,cat_counter[name]] = block.values.codes
            cat_counter[name] += 1
            d[name]['categories'].append(block.values.categories.values)
            d[name]['placement'].append(placement)
        else:
            assert name not in d, '{} name clash'.format(name)
            d[name] = {'values': block.values}
            d[name]['placement'] = placement
    return dict(columns=df.columns.tolist(), blocks=d)

def _get_name(x):
    name = x.dtype.name
    if name == 'category':
        name = (name, x.values.codes.dtype.name)
    else:
        name = ('noncat', name)
    return name

def write_df(df, rootdir):
    meta = breakdown(df)
    write_breakdown(meta, rootdir)

def write_breakdown(meta, rootdir):
    if os.path.exists(rootdir):
        shutil.rmtree(rootdir)
    os.makedirs(rootdir)
    d = meta['blocks']
    announce = lambda x: logging.warn('writing {}'.format(x))
    for name in d:
        base = os.path.join(rootdir, '_'.join(name))
        codes_or_values = 'values'
        if name[0] == 'category':
            for i in range(len(d[name]['categories'])):
                filename = '{}_categories_{}.carray'.format(base, i)
                announce(filename)
                bcolz.carray(d[name]['categories'][i], rootdir=filename)
            d[name].pop('categories')
            codes_or_values = 'codes'
        filename = '{}_{}.carray'.format(base, codes_or_values)
        announce(filename)
        bcolz.carray(d[name][codes_or_values], rootdir=filename)
        d[name].pop(codes_or_values)
    filename = os.path.join(rootdir, 'meta.json')
    announce(filename)
    meta['blocks'] = {'_'.join(k): v for k, v in d.items()} # ugh json
    json.dump(meta, open(filename, 'w'))
    return meta

def read_to_breakdown(rootdir, as_numpy=True):
    meta = json.load(open(os.path.join(rootdir, 'meta.json')))
    d = meta['blocks']
    d = {tuple(k.split('_')): v for k, v in d.items()}
    announce = lambda x: logging.warn('reading {}'.format(x))
    for name in d:
        base = os.path.join(rootdir, '_'.join(name))
        codes_or_values = 'values'
        if name[0] == 'category':
            categories = list()
            for i in range(len(d[name]['placement'])):
                filename = '{}_categories_{}.carray'.format(base, i)
                announce(filename)
                data = bcolz.carray(rootdir=filename)
                categories.append(data[:] if as_numpy else data)
            d[name]['categories'] = categories
            codes_or_values = 'codes'
        filename = '{}_{}.carray'.format(base, codes_or_values)
        announce(filename)
        data = bcolz.carray(rootdir=filename)
        d[name][codes_or_values] = data[:] if as_numpy else data
    meta['blocks'] = d
    return meta

def make_block(values, placement, klass=None, ndim=None, dtype=None,
               fastpath=False):
    if klass is None:
        dtype = dtype or values.dtype
        vtype = dtype.type

        if isinstance(values, SparseArray):
            klass = SparseBlock
        elif issubclass(vtype, np.floating):
            klass = FloatBlock
        elif (issubclass(vtype, np.integer) and
              issubclass(vtype, np.timedelta64)):
            klass = TimeDeltaBlock
        elif (issubclass(vtype, np.integer) and
              not issubclass(vtype, np.datetime64)):
            klass = IntBlock
        elif dtype == np.bool_:
            klass = BoolBlock
        elif issubclass(vtype, np.datetime64):
            if hasattr(values, 'tz'):
                klass = DatetimeTZBlock
            else:
                klass = DatetimeBlock
        elif is_datetimetz(values):
            klass = DatetimeTZBlock
        elif issubclass(vtype, np.complexfloating):
            klass = ComplexBlock
        elif is_categorical(values):
            klass = CategoricalBlock
        else:
            klass = ObjectBlock

    elif klass is DatetimeTZBlock and not is_datetimetz(values):
        return klass(values, ndim=ndim, fastpath=fastpath,
                     placement=placement, dtype=dtype)

    return klass(values, ndim=ndim, fastpath=fastpath, placement=placement)
