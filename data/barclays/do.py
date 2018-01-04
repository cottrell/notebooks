import pandas as pd
import shutil
import datetime
def fix_file(filename):
    rows = [x.strip().split(',', 5) for x in open(filename, encoding='latin-1')]
    bak = '{}.{}'.format(filename, datetime.datetime.today().isoformat())
    print('backed up to {}'.format(bak))
    shutil.copy(filename, bak)
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.to_csv(filename, index=False)

def load_files():
    df = list()
    for f in ['chequing_20140401_20171112.csv', 'saver_20140401_20171113.csv', 'isa_20140401_20171113.csv']:
        df.append(pd.read_csv(f, parse_dates=['Date'], dayfirst=True))
        # print(df[-1].shape)
    return pd.concat(df)

def remove_back_to_back(df):
    d = df.Account.value_counts().index.tolist()
    d = [x.replace('-', '') for x in d]
    def f(x):
        return not any([x.startswith(xx) for xx in d])
    return df[df.Memo.apply(f)]

try:
    df
except NameError as e:
    df = load_files()
    df = remove_back_to_back(df)
    df = df[df.Amount < 0]
    df['Amount'] *= -1
    df['month'] = df.Date.apply(lambda x: datetime.datetime(x.year, x.month, 1))
    df['week'] = df.Date.apply(lambda x: '{}-W{}'.format(x.year, x.week))
    df['dayofweek'] = df.Date.apply(lambda x: x.strftime('%w-%a'))
    d = df.groupby('Date').Amount.sum().sort_index()
    d = d.resample('D').sum().fillna(0)

from pylab import *
ion()
figure(1)
clf()
import matplotlib.gridspec as gridspec
gs = gridspec.GridSpec(2, 2)
ax = subplot(gs[0,:])
d.plot(ax=ax, drawstyle="steps-post", linewidth=2, label='daily', alpha=0.5)
nn = 30
dd = d.rolling(window=nn).sum()
# dd = d.ewm(halflife=nn).mean() * 30
# dd = d.cumsum() / range(1, d.shape[0]+1) * 30
dd.plot(ax=ax, linewidth=1, label='last {} days'.format(nn))
# a = d.copy()
# a[:] = 0
# a.plot()
title('spend')
grid()
# savefig('fig.png')
legend()
show()
ax = subplot(gs[1,0])
d.groupby(d.index.dayofweek).mean().plot(ax=ax, kind='bar')
title('mean weekdays')
ax = subplot(gs[1,1])
d.groupby(d.index.month).mean().plot(ax=ax, kind='bar')
title('mean weekdays')
