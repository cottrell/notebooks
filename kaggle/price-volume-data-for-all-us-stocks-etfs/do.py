#!/usr/bin/env python
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

_mydir = os.path.dirname(os.path.realpath(__file__))

def raw_source():
    return glob.glob(os.path.join(_mydir, k, '*.txt.gz'))

def raw_target(nrows=None):
    return os.path.join(_mydir, 'nrows={}'.format(nrows if nrows is not None else 'all'))

def run_raw(nrows=None, force=False):
    """ parse the data, save a parquet """
    # not a lot of data here ... do it in memory, forget about parallelism
    outfile = raw_target(nrows=nrows)
    if force:
        if os.path.exists(outfile):
            shutil.rmtree(outfile)
    if not os.path.exists(outfile):
        for k in ['ETFs', 'Stocks']:
            data = list()
            product = k.lower()
            filenames = raw_source()
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
            # pq.write_table(table, outfile)
            # df.to_parquet(outfile, index=False)
    # print('reading {}'.format(outfile))
    # return pd.read_parquet(outfile)

_rolling_days = [30, 60]

def enriched_source(nrows=None):
    return raw_target(nrows=nrows)

def enriched_target(nrows=None):
    return os.path.join(_mydir, 'enriched/nrows={}'.format(nrows if nrows is not None else 'all'))

def enrich_pandas_single(df, inplace=True):
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
            df['future_' + k + '_rolling_min_{}d'.format(i)] = df[k + '_rolling_min_{}d'.format(i)].shift(-i)
            df['future_' + k + '_rolling_max_{}d'.format(i)] = df[k + '_rolling_min_{}d'.format(i)].shift(-i)
    return df

import dask.bag as db
def run_enriched(nrows=None):
    input_dirname = enriched_source(nrows=nrows)
    filenames = glob.glob(os.path.join(input_dirname, 'product=etfs/name=*/')) # limit to etfs for now
    output_dirname = enriched_target(nrows=nrows)
    if os.path.exists(output_dirname):
        os.system('dl {}'.format(output_dirname))
    bag = db.from_sequence(filenames)
    output_filenames = bag.map(lambda x: os.path.join(output_dirname, os.path.relpath(x, input_dirname))).compute() # no need for delayed on glob really
    def read_transform_write(infile, outfile):
        print('{} -> {}'.format(infile, outfile))
        df = pd.read_parquet(infile)
        enrich_pandas_single(df, inplace=True)
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_to_dataset(table, root_path=outfile, preserve_index=False)
    mapped = db.from_sequence(zip(filenames, output_filenames)).starmap(read_transform_write)
    mappend.compute()

# def enrich(df):
#     import pyspark.sql.functions as F
#     todrop = ['market', 'OpenInt']
#     df = df.drop(*todrop)
#     df = df.withColumn('Date', F.col('Date').cast('date'))
#     df = df.orderBy(['product', 'name', 'Date'])
#     # df = df.repartition('product', 'name')
#     # return df
#     # TODO repartition somehow and figure out why slow
#     for i in [30, 60, 90]:
#         d = df[['product', 'name', 'Date', 'Close']].withColumn('Date', F.date_add(F.col('Date'), i)).withColumnRenamed('Close', 'close_{}d'.format(i))
#         df = df.join(d, on=['product', 'name', 'Date'], how='left')
#     return df

# def spark_part(outdir=None, nrows=None):
#     """ read the origin and parition it """
#     # for fun, not fast
#     import mylib.spark
#     sc, spark = mylib.spark.get_spark_context_and_session()
#     filename = os.path.join(_mydir, 'nrows={}'.format(nrows if nrows is not None else 'all'))
#     if outdir is None:
#         outdir = os.path.join(_mydir, 'enriched/nrows=all')
#     if os.path.exists(outdir):
#         os.system('dl {}'.format(outdir))
#     df = spark.read.parquet(filename)
#     df = enrich(df)
#     print('writing {}'.format(outdir))
#     df.write.partitionBy('product').parquet(outdir)

if __name__ == '__main__':
    argh.dispatch_commands([run_raw, run_enriched])
