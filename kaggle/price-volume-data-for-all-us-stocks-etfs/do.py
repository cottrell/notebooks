#!/usr/bin/env python
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

def run(nrows=None, force=False):
    """ parse the data, save a parquet """
    # not a lot of data here ... do it in memory, forget about parallelism
    outfile = os.path.join(_mydir, 'nrows={}'.format(nrows if nrows is not None else 'all'))
    if force:
        if os.path.exists(outfile):
            shutil.rmtree(outfile)
    if not os.path.exists(outfile):
        for k in ['ETFs', 'Stocks']:
            data = list()
            product = k.lower()
            filenames = glob.glob(os.path.join(_mydir, k, '*.txt.gz'))
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
            print('writing {}'.format(outfile))
            # plain to_parquet seems to be always writing the index, also partition_cols not in pandas yet
            table = pa.Table.from_pandas(df, preserve_index=False)
            pq.write_to_dataset(table, root_path=outfile, partition_cols=['product'], preserve_index=False)
            # pq.write_table(table, outfile)
            # df.to_parquet(outfile, index=False)
    # print('reading {}'.format(outfile))
    # return pd.read_parquet(outfile)

def spark_part(nrows=None):
    """ read the origin and parition it """
    # for fun, not fast
    import mylib.spark
    import pyspark.sql.functions as F
    sc, spark = mylib.spark.get_spark_context_and_session()
    filename = os.path.join(_mydir, 'nrows={}'.format(nrows if nrows is not None else 'all'))
    outdir = os.path.join(_mydir, 'enriched/nrows=all')
    if os.path.exists(outdir):
        os.system('dl {}'.format(outdir))
    df = spark.read.parquet(filename)
    todrop = ['market', 'OpenInt', '__index_level_0__']
    df = df.drop(*todrop)
    df = df.withColumn('Date', F.col('Date').cast('date'))
    df = df.repartition('name')
    # return df
    # TODO repartition somehow and figure out why slow
    for i in [30, 60, 90]:
        d = df[['Date', 'name', 'Close']].withColumn('Date', F.date_add(F.col('Date'), i)).withColumnRenamed('Close', 'close_{}d'.format(i))
        df = df.join(d, on=['Date', 'name'], how='left')
    df.repartition('product').write.partitionBy('product').parquet(outdir)


if __name__ == '__main__':
    argh.dispatch_commands([run, spark_part])
