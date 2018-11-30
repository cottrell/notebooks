#!/usr/bin/env python
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

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override()

_mydir = os.path.dirname(os.path.realpath(__file__))

def raw_source(dirname):
    return glob.glob(os.path.join(_mydir, dirname, '*.txt.gz'))

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
        df = df.drop(['market', 'OpenInt'], axis=1)
        df.columns = [x.lower() for x in df.columns]
        print('writing {}'.format(outfile))
        # plain to_parquet seems to be always writing the index, also partition_cols not in pandas yet
        table = pa.Table.from_pandas(df, preserve_index=False)
        # partitioning by name is less efficient storage wise but makes for better joins in the next step
        pq.write_to_dataset(table, root_path=outfile, partition_cols=['product', 'name'], preserve_index=False)

def download_update_target():
    return os.path.join(_mydir, 'update')

def download_update(force=False):
    input_dirname = raw_target()
    product = 'etfs'
    filenames = glob.glob(os.path.join(input_dirname, 'product={}/name=*/'.format(product))) # limit to etfs for now
    for filename in filenames:
        name, market = os.path.basename(filename).split('.')[:2]
        df = download_update_one_from_yahoo(name, product)

def download_update_one_from_yahoo(name, product, start_date=None, end_date=None):
    # example tan, if start_date is None use last avail date in the raw data
    # if end_date is None:
    #     end_date = datetime.datetime.today().date()
    input_dirname = download_update_target()
    filename = os.path.join
    if start_date is None:
        # get start date from raw
        filename = os.path.join(raw_target(), 'product={}/name={}'.format(product, name))
        start_date = pd.read_parquet(filename).date.max()
        start_date = start_date.date() + datetime.timedelta(days=1)
    df = pdr.get_data_yahoo([name], start=start_date, end=end_date)
    return df


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
