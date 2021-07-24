"""
See https://gist.github.com/cottrell/a3f95aa59408d87f925ec606d8783e62

$ uname -a
Linux ip-??? ???-aws #53-Ubuntu SMP Wed Sep 18 13:35:53 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
$ python --version
Python 3.7.3
$ pip list
Package         Version   Location
--------------- --------- -----------------------------
certifi         2019.9.11
memory-profiler 0.55.0
numpy           1.17.3
pandas          0.25.2
pip             19.3.1
psutil          5.6.3
pyarrow         0.15.0
python-dateutil 2.8.0
pytz            2019.3
setuptools      41.4.0
six             1.12.0
wheel           0.33.6

$ pip install memory-profiler
$ mprof run memory_leak_parquet.py
$ mprof plot
"""
import datetime
import pandas as pd
import pyarrow.parquet as pq
import os
import gi
import numpy as np
import glob

filename = 'data.parquet'
if not os.path.exists(filename):
    print(f'creating {filename}')
    import random
    import string
    def randomString(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    m = 15000
    temp = np.random.randn(m, 60)
    temp = np.where(temp < -0.1, np.nan, temp)
    df = pd.DataFrame(temp)
    arity = 2000
    for k in ['A', 'B', 'C']:
        temp = [None] + [randomString(1000) for i in range(arity - 1)]
        df[k] = [temp[i] for i in np.random.randint(0, arity, m)]
    df['bool'] = True
    df['date'] = datetime.date.today()
    df.columns = [str(x) for x in df.columns]
    df.to_parquet(filename)
    print('created file on first pass, run again to test.')
else:
    n = 300
    print(f'reading {filename} {n} times')
    for i in range(n):
        print(i)
        # df = pd.read_parquet(filename)
        df = pq.ParquetDataset(filename).read().to_pandas()
