#!/usr/bin/env python
from ratelimit import limits, sleep_and_retry
import json
import time
import bcolz
import numpy as np
import datetime
import argh
import pandas as pd
import time
import glob
import os
import mylib.io
import pyarrow as pa
import pyarrow.parquet as pq
import shutil
import dask.bag as db
from joblib import Memory


from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override()

_mydir = os.path.dirname(os.path.realpath(__file__))

cachedir = os.path.join(_mydir, 'joblib_cache')
memory = Memory(cachedir, verbose=1)

# WARNING: persistant state here, clear if worried
_period_seconds = 1
@memory.cache
@sleep_and_retry
@limits(calls=1, period=_period_seconds)
def _get_data_yahoo(names, start, end):
    return pdr.get_data_yahoo(names, start=start, end=end)

def get_data_yahoo(names, start, end):
    df = _get_data_yahoo(names, start, end)
    if len(names) > 1:
        df = df.stack()
        df.index.names = ['date', 'name']
    else:
        df['name'] = names[0]
    df = df.reset_index()
    df.columns = [x.lower().replace(' ', '_') for x in df.columns]
    return df

def one_off_update(product='etfs'):
    start = datetime.date(2010, 1, 1)
    end = datetime.date(2018, 11, 29)
    names = _meta[product]
    base = os.path.join('raw/yahoo/')
    if not os.path.exists(base):
        os.makedirs(base)

    # filenames = glob.glob(os.path.join(base, '*.parquet'))
    # TODO: check dates on existing for the update

    filename = os.path.join(base, '{}_to_{}'.format(start, end))
    filename_check = os.path.join(filename, 'product={}'.format(product)) # this is terrible
    if os.path.exists(filename_check):
        print("{} exists".format(filename_check))
        return
    print('getting {} names'.format(len(names)))
    df = get_data_yahoo(names, start, end)
    df['product'] = product
    table = pa.Table.from_pandas(df, preserve_index=False)
    # partitioning by name is less efficient storage wise but makes for better joins in the next step
    pq.write_to_dataset(table, root_path=filename, partition_cols=['product', 'name'], preserve_index=False)
    return df



### IGNORE OLD except for comparison?


def raw_source(dirname):
    return glob.glob(os.path.join(_mydir, 'raw', dirname, '*.txt.gz'))

def raw_target(nrows=None):
    return os.path.join(_mydir, 'nrows={}'.format(nrows if nrows is not None else 'all'))

def run_raw(nrows=None, force=False):
    """ parse the data, save a parquet """
    # not a lot of data here ... do it in memory, forget about parallelism
    outfile = raw_target(nrows=nrows)
    if force:
        if os.path.exists(outfile):
            shutil.rmtree(outfile)
    if os.path.exists(outfile):
        print('{} exists. force=True to rerun'.format(outfile))
        return
    for k in ['ETFs', 'Stocks']:
        data = list()
        product = k.lower()
        filenames = raw_source(k)
        t = time.time()
        i = 0
        for filename in filenames:
            name, market = os.path.basename(filename).split('.')[:2]
            product, market, name, filename, dict(nrows=nrows)
            lc = mylib.io.get_capped_line_count(filename)
            if lc >= 2:
                df = pd.read_csv(filename, nrows=nrows, encoding='utf-8')
                df['product'] = product
                df['market'] = market
                df['name'] = name
                df['Date'] = pd.to_datetime(df.Date)
                data.append(df)
            else:
                print('skipping {}'.format(filename))
            i += 1
            if i % 10 == 0:
                print('{} of {} eta {} seconds for {}'.format(i, len(filenames), (time.time() - t) * (len(filenames) - i) / i, product))
        df = pd.concat(data, axis=0)
        df = df.sort_values(['name', 'Date'])
        # TODO: add market back later if relevant
        df = df.drop(['market', 'OpenInt'], axis=1)
        df.columns = [x.lower() for x in df.columns]
        print('writing {}'.format(outfile))
        # plain to_parquet seems to be always writing the index, also partition_cols not in pandas yet
        table = pa.Table.from_pandas(df, preserve_index=False)
        # partitioning by name is less efficient storage wise but makes for better joins in the next step
        pq.write_to_dataset(table, root_path=outfile, partition_cols=['product', 'name'], preserve_index=False)

_meta_filename = os.path.join(_mydir, 'meta.json')
_meta = json.load(open(_meta_filename))

# def raw_symlink_target():
#     return os.path.join('raw/symlink')
# 
# def raw_symlink_concat():
#     target_base = raw_symlink_target()
#     raw = raw_target()
#     update = download_update_target()
#     allkeys = ['product={}/name={}'.format(product, name) for product, names in _meta.items() for name in names]
#     for base in [raw, update]:
#         for k in allkeys:
#             pattern = os.path.join(base, k, '*.parquet')
#             filenames = glob.glob(pattern)
#             for source in filenames:
#                 target = os.path.join(target_base, k, os.path.basename(source))
#                 print(source, target)
#                 if not os.path.exists(target) and os.path.exists(source):
#                     source = os.path.relpath(source, os.path.dirname(target))
#                     os.makedirs(os.path.dirname(target), exist_ok=True)
#                     os.symlink(source, target)

def download_update_target():
    dirname = os.path.join(_mydir, 'raw', 'update')
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

def download_update(force=False):
    input_dirname = raw_target() # nrows=all or raw_source?
    product = 'etfs' # TODO: only etfs for now
    filenames = glob.glob(os.path.join(input_dirname, 'product={}/name=*'.format(product))) # limit to etfs for now
    for filename in filenames:
        # TODO: ignoring market for now
        name = os.path.basename(filename).split('=')[1]
        print('download_update {} ignoring market (since everything is from US for now)'.format(name))
        try:
            download_update_one_from_yahoo(product, name)
        except ValueError as e:
            print("skipping error {} but adding to list of bad tickers".format(e))
            if not os.path.exists('failed_updates'):
                os.makedirs('failed_updates')
            print(product, name, file=open(os.path.join('failed_updates', name), 'w'))

def get_missing_dates(product, name):
    # get start date from raw_target() and update
    # TODO: actually do bdate range or whatever, currently making hard assumption of continuity in dates
    missing_back_dates = [] # TODO: backfill check biz days etc
    filename = os.path.join(raw_target(), 'product={}/name={}'.format(product, name))
    first_new_date = pd.read_parquet(filename).date.max()
    filename = os.path.join(download_update_target(), 'product={}/name={}'.format(product, name))
    if len(glob.glob(os.path.join(filename, '*.parquet'))) > 0:
        first_new_date = max(first_new_date, pd.read_parquet(filename).date.max())
    first_new_date = first_new_date.date() + datetime.timedelta(days=1)
    return missing_back_dates, first_new_date


def download_update_one_from_yahoo(product, name, start_date=None, end_date=None):
    # example tan, if start_date is None use last avail date in the raw data
    output_dirname = download_update_target()
    filename = os.path.join
    if start_date is None:
        missing_back_dates, start_date = get_missing_dates(product, name)
    # TODO: worrying about exact timing
    if start_date >= (datetime.date.today() - datetime.timedelta(days=1)):
        print("{} {} has data up to but not including {}".format(product, name, start_date))
        return
    df = get_data_yahoo([name], start=start_date, end=end_date)
    if missing_back_dates:
        raise Exception('nip')
    print('writing {}'.format(output_dirname))
    df['product'] = product # TODO: better ways to do this but this is safer
    df['name'] = name # TODO: better ways to do this but this is safer
    df = df.reset_index()
    df.columns = [x.lower() for x in df.columns]
    table = pa.Table.from_pandas(df, preserve_index=False)
    # this CAN lead to duplicate entries so deduping is necessary, idea is that this is basically append-only like
    pq.write_to_dataset(table, root_path=output_dirname, partition_cols=['product', 'name'], preserve_index=False)
    # return df

# enrichment only

def calc_rank_quantile_source(nrows=None):
    return raw_target(nrows=nrows)

def calc_rank_quantile_target(nrows=None):
    return os.path.join(_mydir, 'calc_rank_quantile/nrows={}'.format(nrows if nrows is not None else 'all'))

def calc_rank_quantile_single(df):
    pass

def run_calc_rank_quantile(nrows=None, force=False):
    pass

_rolling_days = [30, 60]

def enriched_source(nrows=None):
    return raw_target(nrows=nrows)

def enriched_target(nrows=None):
    return os.path.join(_mydir, 'enriched/nrows={}'.format(nrows if nrows is not None else 'all'))

def enrich_pandas_single(df, inplace=True):
    # single means one ticker, we are mapping across the tickers
    if not inplace:
        df = df.copy()
    # don't bother with filling in dates, ideally want to include time as feature
    # min_date, max_date = df.Date.min(), df.Date.max()
    # date_range = pd.date_range(min_date, max_date)
    # df = df.set_index('Date').reindex(date_range)
    for k in ['weekday', 'day', 'month', 'year']:
        df[k] = getattr(df['date'].dt, k)
    for i in _rolling_days:
        r = df.rolling(i)
        for k in ['close']:
            df[k + '_rolling_min_{}d'.format(i)] = r[k].min()
            df[k + '_rolling_max_{}d'.format(i)] = r[k].max()
            # the min/max returns on a i-day period
            df['future_' + k + '_max_loss_{}d'.format(i)] = df[k + '_rolling_min_{}d'.format(i)].shift(-i) / df.close - 1
            df['future_' + k + '_max_gain_{}d'.format(i)] = df[k + '_rolling_max_{}d'.format(i)].shift(-i) / df.close - 1
    return df

def run_enriched(nrows=None, force=False):
    """ enrich for each ticker. map compute via dask bag. This is just column extension, row-length should be same """
    input_dirname = enriched_source(nrows=nrows)
    filenames = glob.glob(os.path.join(input_dirname, 'product=etfs/name=*/')) # limit to etfs for now
    output_dirname = enriched_target(nrows=nrows)
    if force and os.path.exists(output_dirname):
        shutil.rmtree(output_dirname)
    if os.path.exists(output_dirname):
        print('{} exists. force=True to rerun'.format(output_dirname))
        return
    bag = db.from_sequence(filenames)
    output_filenames = bag.map(lambda x: os.path.join(output_dirname, os.path.relpath(x, input_dirname))).compute() # no need for delayed on glob really
    def read_transform_write(infile, outfile):
        print('{} -> {}'.format(infile, outfile))
        df = pd.read_parquet(infile)
        enrich_pandas_single(df, inplace=True)
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_to_dataset(table, root_path=outfile, preserve_index=False)
    mapped = db.from_sequence(zip(filenames, output_filenames)).starmap(read_transform_write)
    mapped.compute()

_min_date = datetime.datetime(2006, 1, 1)
_max_date = datetime.datetime(2017, 11, 10)
_validation_cutoff = datetime.datetime(2016, 1, 1)

def get_xy_data_plain(df_in, n_steps_back=10, validation_date=_validation_cutoff):
    # takes ~77 ms on qqq which has about ~4k rows
    if validation_date is not None:
        is_validation_set = df_in.date >= validation_date
        df_train, df_val = df_in[~is_validation_set], df_in[is_validation_set]
        X_train, y_train = get_xy_data_plain(df_train, n_steps_back=n_steps_back, validation_date=None)
        X_val, y_val = get_xy_data_plain(df_val, n_steps_back=n_steps_back, validation_date=None)
        return X_train, y_train, X_val, y_val

    # FOR ONE NAME ONLY AT A TIME! this is just to look at autogressive performance
    # LSTM format not, unrolled for plain regression or signatured for iis
    # ycols = [x for x in df.columns if 'future_' in x]
    # ycols = ['future_close_max_loss_30d', 'future_close_max_gain_30d', 'future_close_max_loss_60d', 'future_close_max_gain_60d'] 
    ycols = ['future_close_max_loss_60d']
    # xcols = ['open', 'high', 'low', 'close', 'volume', 'weekday', 'day', 'month', 'year', 'close_rolling_min_30d', 'close_rolling_max_30d', 'close_rolling_min_60d', 'close_rolling_max_60d']
    xcols = ['t', 'close', 'volume', 'close_rolling_min_30d', 'close_rolling_max_30d', 'close_rolling_min_60d', 'close_rolling_max_60d']
    df = df_in.dropna(subset=ycols, how='any').copy() # need copy otherwise get warnings
    df.loc[:,xcols[1:]] = np.log(df[xcols[1:]])
    df.loc[:,'t'] = (df.date - df.date.min()).dt.days
    df.loc[:,xcols] = df[xcols].diff() # use the increments? dunno
    df = df.dropna(subset=ycols + xcols)
    yy = df[ycols].values
    xx = df[xcols].values
    # NOTE: YOU SHOULD NOTE USE t UNLESS YOU ARE USING THE dt IN THE SIGNATURE OR UNROLLED VERION OR SOMETHING LIKE THAT
    X = list()
    y = list()
    for i in range(n_steps_back, df.shape[0]):
        X.append(xx[i-n_steps_back:i].flatten())
        y.append(yy[i])
    X = np.array(X)
    y = np.array(y)
    return X, y

# so we want to to try various models on the data, start with one name only, there are many train/test/val strategies. take simplest first.
# main point is to make this easily swappable with different models. Some models with require data transformations to make them work.
# start with the easiest ones first that don't require ANY data scaling (trees)
# really would be best to look at modeldb for this

def get_sample_data():
    """
    reload(do); globals().update(do.get_sample_data())
    """
    df = pd.read_parquet('enriched/nrows=all/product=etfs/name=qqq')
    X_train, y_train, X_val, y_val = get_xy_data_plain(df)
    return locals()

if __name__ == '__main__':
    argh.dispatch_commands([run_raw, run_enriched])
