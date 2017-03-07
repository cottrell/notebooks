import asyncio
import time
import os
import pandas as pd
import mylib.data # setup.py in notebooks
import mylib.tools as tools
from numpy.random import randn
import string

# _s = dict(str=['a'], float=['b', 'c', 'd', 'e'])
# _s = tools.dict_of_lists_to_dict(_s)
_s = {'a': 'str', 'b': 'float', 'c': 'float', 'd': 'float', 'e': 'float'}
_s = tools.dict_to_spark_schema(_s)

def gen_data(m=10, n=4):
    df = pd.DataFrame(randn(m, n + 1))
    df.columns = list(string.ascii_lowercase[:n + 1])
    df['a'] = [mylib.data.id_generator(m) for x in range(m)]
    df = df.set_index('a')
    return df

def periodically_generate_new_data():
    return tools.run_in_background(_periodically_generate_new_data)

def _periodically_generate_new_data(period=5, nmax=100, basedir='./data'):
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
        # print('asdf {} {}'.format(t, filename))
        df.to_csv(filename, compression='gzip')
        time.sleep(period)

if __name__ == '__main__':
    pass
