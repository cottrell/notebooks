import os
import glob
import subprocess
import pandas as pd
import shutil
import datetime
_mydir = os.path.dirname(os.path.realpath(__file__))
def fix_file(filename):
    rows = [x.strip().split(',', 5) for x in open(filename, encoding='latin-1')]
    bak = '{}.{}'.format(filename, datetime.datetime.today().isoformat())
    print('backed up to {}'.format(bak))
    shutil.copy(filename, bak)
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.to_csv(filename, index=False)

def confirm_do_this(msg='are you sure?'):
    res = input(msg + ' y[n] : ')
    if res == 'y':
        return True
    else:
        return False

def load_files():
    df = list()
    # just update whole set each time
    files = [glob.glob(x)[-1] for x in ['chequing_20140401_20??????.csv', 'saver_20140401_20??????.csv', 'isa_20140401_20??????.csv']]
    print('found files {}'.format(files))
    for f in files:
        try:
            temp = pd.read_csv(f, parse_dates=['Date'], dayfirst=True)
        except Exception as e:
            print('got exception reading {} {}'.format(f, e))
            print('usually this is because you need to strip the first column or something like that. The file looks like this:')
            subprocess.call('cat {} | head'.format(os.path.join(_mydir, f)), shell=True)
            if confirm_do_this(msg='Do you want to run the fixer and then try to read the file again? File will be backed up with a timestamped version?'):
                fix_file(f)
                temp = pd.read_csv(f, parse_dates=['Date'], dayfirst=True)
            else:
                raise e
        df.append(temp)
        # print(df[-1].shape)
    df = pd.concat(df)
    # there is no good way to do this, just repull the full datasets
    # dupes = df[df.duplicated()]
    # if dupes.shape[0] > 0:
    #     print('dropping {} dupes:'.format(len(dupes)))
    #     print(dupes)
    #     df = df.drop_duplicates()
    return df

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
    # spend is only interesting thing really
    df = df[df.Amount < 0]
    df['Amount'] *= -1
    df['month'] = df.Date.apply(lambda x: datetime.datetime(x.year, x.month, 1))
    df['week'] = df.Date.apply(lambda x: '{}-W{}'.format(x.year, x.week))
    df['dayofweek'] = df.Date.apply(lambda x: x.strftime('%w-%a'))
    d = df.groupby('Date').Amount.sum().sort_index()
    d = d.resample('D').sum().fillna(0)

from pylab import *
import matplotlib.gridspec as gridspec
def doplot():
    ion()
    figure(1)
    clf()
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
    ax = subplot(gs[1,0])
    d.groupby(d.index.dayofweek).mean().plot(ax=ax, kind='bar')
    title('mean weekdays')
    ax = subplot(gs[1,1])
    d.groupby(d.index.month).mean().plot(ax=ax, kind='bar')
    title('mean weekdays')
    show()

def top_things(df):
    a = df.sort_values('Amount', ascending=False)
    a.index = range(a.shape[0])
    noninteresting = (a.Memo.str.match('^PEACH.*|^VIEW.*|^A A B.*')).values
    return a[~noninteresting]

def top_recent_things(df):
    a = top_things(df)
    # big things last n days
    n = 6 * 30
    start_date = df.Date.max() - datetime.timedelta(days=n)
    i = (a.Date > start_date).values
    return a[i].head(n=30).sort_values('Date', ascending=False)

doplot()
print("\ntop recent things")
print(top_recent_things(df))
print("\ntop things all time")
print(top_things(df).head(n=30))


