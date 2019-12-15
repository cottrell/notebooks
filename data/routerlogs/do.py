#!/usr/bin/env python
import datetime
import pandas as pd
df = pd.read_csv('timeseries.csv')
# df['date'] = df.date.apply(lambda x: datetime.datetime.strptime(x, '%A, %B %d,%Y %H:%M:%S'))
df['date'] = df.date.apply(lambda x: pd.to_datetime(x))
df['ip'] = df.ip.apply(lambda x: x.split(':')[0])
df['dt'] = df.date.dt.round('1min')
d = df.groupby(['dt', 'ip']).size()
print(d.shape)
print(d.to_string())
d.unstack('ip').fillna(0).plot()
from pylab import *
ion()
savefig('a.png')
