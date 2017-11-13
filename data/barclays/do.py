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

df = load_files()
df['month'] = df.Date.apply(lambda x: datetime.datetime(x.year, x.month, 1))
d = df.groupby('month').Amount.sum().sort_index()
from pylab import *
ion()
figure(1)
clf()
ax = subplot(111)
d.plot(ax=ax, drawstyle="steps-post", linewidth=2)
a = d.copy()
a[:] = 0
a.plot()

