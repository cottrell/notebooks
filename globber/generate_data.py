#!/usr/bin/env python
import logging
import string
import os
import time
import argh
import pandas as pd
import mylib
import mylib.tools
import mylib.data
from numpy.random import randn, permutation

_s_orig = dict(str=['a', 'f', 'g'], float=['b', 'c', 'd', 'e'])
_s = mylib.tools.dict_of_lists_to_dict(_s_orig)
_n = len(_s)

def gen_data(m=10, n=_n):
    df = pd.DataFrame(randn(m, n))
    df.columns = list(string.ascii_lowercase[:n])
    for k in _s_orig['str']:
        df[k] = [mylib.data.id_generator(m) for x in range(m)]
    df = df.set_index('a')
    return df

def periodically_generate_new_data():
    return mylib.tools.run_in_background(_periodically_generate_new_data)

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
        logging.info('WRITE: {} {}'.format(t, filename))
        df.to_csv(filename, compression='gzip')
        time.sleep(period)

if __name__ == '__main__':
    argh.dispatch_command(_periodically_generate_new_data)
