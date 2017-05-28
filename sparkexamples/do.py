#!/usr/bin/env python
import asyncio
import argh
import time
import os
import pandas as pd
import mylib.data # setup.py in notebooks
import mylib.tools as tools
from numpy.random import randn, permutation
import string
import glob
import gzip
import collections

def _get_headers(files):
    d = list()
    for f in files:
        if f.endswith('.gz'):
            fin = gzip.open(f)
        else:
            fin = open(f)
        header = fin.readline().strip().decode()
        d.append((header, f))
    return d

class SparkParser():
    def __init__(self, globber, sep=',', schema=None, header=True, csv_args=None):
        self.globber = globber
        self.sep = sep
        if csv_args is None:
            csv_args = dict()
        self.csv_args = csv_args
        self.schema = schema
        self.header = header
    def parse(self):
        # this is dumb
        files = self.globber()
        if self.header:
            d = _get_headers(files)
            first_header = d[0][0].split(self.sep)
            d = tools.list_of_tuples_to_dict_of_lists(d)
            tasks = list()
            for header, files in d.items():
                header = header.split(self.sep)
                schema = self.schema
                if schema is not None:
                    schema = tools.reorder_schema(schema, header)
                tasks.append((schema, files))
            spark_tasks = list()
            from pyspark.sql.session import SparkSession
            spark = SparkSession.builder.getOrCreate()
            for schema, files in tasks:
                task = spark.read.csv(files, header=self.header,
                        sep=self.sep, schema=schema, **self.csv_args)
                spark_tasks.append(task)
            return spark_tasks
        else:
            raise Exception('no header you do not need this wrapper')

_s_orig = dict(str=['a', 'f', 'g'], float=['b', 'c', 'd', 'e'])
_s = tools.dict_of_lists_to_dict(_s_orig)
_n = len(_s)
_s = tools.dict_to_spark_schema(_s)

sp = SparkParser(
        lambda : glob.glob('data/*.csv.gz'),
        schema=_s)

def gen_data(m=10, n=_n):
    df = pd.DataFrame(randn(m, n))
    df.columns = list(string.ascii_lowercase[:n])
    for k in _s_orig['str']:
        df[k] = [mylib.data.id_generator(m) for x in range(m)]
    df = df.set_index('a')
    return df

def periodically_generate_new_data():
    return tools.run_in_background(_periodically_generate_new_data)

def _periodically_generate_new_data(period=5, nmax=100, basedir='./data', scramble_columns=True):
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    dt = 1
    if nmax is None:
        dt = 0
    t = 0
    file_counter = 0
    while t < nmax:
        df = gen_data()
        if scramble_columns:
            df = df.iloc[:,permutation(df.shape[1])]
        filename = os.path.join(basedir, '{}.csv.gz'.format(file_counter))
        file_counter += 1
        t += dt
        # print('asdf {} {}'.format(t, filename))
        df.to_csv(filename, compression='gzip')
        time.sleep(period)

if __name__ == '__main__':
    argh.dispatch_command(_periodically_generate_new_data)
