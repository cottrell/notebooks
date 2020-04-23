import pandas as pd
from pylab import *
df = pd.read_csv('88e36d71-d843-4cf8-9b4d-68fad9bf6be3.csv')
df['Statistics'] = df.Statistics.map(lambda x: int(x[:2]) / 100)
s = df.set_index(['Geography', 'Sex', 'Earnings_codelist', 'Statistics', 'Time']).V4_2.unstack('Statistics').loc[['London', 'Inner London']]

ion()
figure(1)
clf()
ax = gca()
ss = s.groupby(['Sex', 'Geography', 'Earnings_codelist']).max()
ss.xs('Male', level='Sex', drop_level=False).T.plot(ax=ax, style='--')
ss.xs('Female', level='Sex', drop_level=False).T.plot(ax=ax, style='-')
grid()
show()
