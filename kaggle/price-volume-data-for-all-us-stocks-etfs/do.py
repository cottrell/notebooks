#!/usr/bin/env python
import argh
import pandas as pd
import time
import glob
import os
import mylib.io

_mydir = os.path.dirname(os.path.realpath(__file__))

def run(nrows=None, force=False):
    """ parse the data, save a parquet """
    # not a lot of data here ... do it in memory, forget about parallelism
    data = list()
    outfile = os.path.join(_mydir, 'nrows={}.parquet'.format(nrows if nrows is not None else 'all'))
    if not os.path.exists(outfile) or force:
        for k in ['ETFs', 'Stocks']:
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
                    # data.append((product, market, name, filename, df))
                    data.append(df)
                else:
                    print('skipping {}'.format(filename))
                i += 1
                if i % 10 == 0:
                    print('{} of {} eta {} seconds for {}'.format(i, len(filenames), (time.time() - t) * (len(filenames) - i) / i), product)
        df = pd.concat(data, axis=0)
        print('writing {}'.format(outfile))
        df.to_parquet(outfile)
    print('reading {}'.format(outfile))
    return pd.read_parquet(outfile)

def spark_part():
    """ read the origin and parition it """
    # for fun
    import mylib.spark
    sc, spark = mylib.spark.get_spark_context_and_session()
    filename = os.path.join(_mydir, 'nrows=all.parquet')
    outdir = os.path.join(_mydir, 'nrows=all')
    spark.read.parquet(filename).write.partitionBy('product').parquet(outdir)

if __name__ == '__main__':
    argh.dispatch_commands([run, spark_part])
