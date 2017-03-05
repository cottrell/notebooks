import asyncio
import os
import pandas as pd
import mylib.data # setup.py in notebooks
import mylib.tools as tools
from numpy.random import randn
import string

def gen_data(m=10, n=4):
    df = pd.DataFrame(randn(m, n + 1))
    df.columns = list(string.ascii_lowercase[:n + 1])
    df['a'] = mylib.data.id_generator(m)
    df = df.set_index('a')
    return df

def periodically_generate_new_data():
    return tools.schedule_coroutine(_periodically_generate_new_data())

async def _periodically_generate_new_data(period=5, nmax=100, basedir='./data'):
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    dt = 1
    if nmax is None:
        dt = 0
    t = 0
    file_counter = 0
    while t < nmax:
        df = gen_data()
        filename = os.path.join(basedir, '{}.csv.gz'.format(file_counter))
        file_counter += 1
        t += dt
        print('asdf {} {}'.format(t, filename))
        df.to_csv(filename, compression='gzip')
        await asyncio.sleep(period)

import itertools
async def ticker():
    for i in itertools.count():
        await asyncio.sleep(1)



