import os
import numpy as np
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

def get_noninteresting_mask(a):
    return (a.Memo.str.match('^PEACH.*|^VIEW.*|^A A B.*')).values

def is_transfer(df):
    return df.Memo.str.startswith('QI').values


try:
    df
except NameError as e:
    df = load_files()
    df = remove_back_to_back(df)
    # spend is only interesting thing really
    df['Amount_in'] = np.where(df.Amount > 0, df.Amount, 0)
    df['Amount'] = np.where(df.Amount < 0, df.Amount, 0)
    df['Amount'] *= -1
    df['month'] = df.Date.apply(lambda x: datetime.datetime(x.year, x.month, 1))
    df['week'] = df.Date.apply(lambda x: '{}-W{}'.format(x.year, x.week))
    df['dayofweek'] = df.Date.apply(lambda x: x.strftime('%w-%a'))
    noninteresting = get_noninteresting_mask(df)
    is_transfer_ = is_transfer(df)
    df['rental'] = np.where(noninteresting, df.Amount.values, 0)
    df['transfer'] = np.where(is_transfer_, df.Amount.values, 0)
    df['Amount_orig'] = df.Amount.copy()
    df['Amount'] = df.Amount - df.rental - df.transfer
    df['Amount_out'] = df.Amount + df.rental + df.transfer
    df['taxyear'] = np.where(df.Date.apply(lambda x: x < datetime.datetime(x.year, 4, 6)).values, df.Date.dt.year - 1, df.Date.dt.year)
    df['taxyear'] = df.taxyear.apply(lambda x: str(x) + '-' + str(x+1)[-2:])
    df['check'] = df.Amount_out == df.Amount_orig
    assert df.check.all()

    print('exclude initial by hard code')
    df = df[(df.Memo != '14CANARY WHARF BRA REM') & (df.Date != '2014-06-10')]



from pylab import *
import matplotlib.gridspec as gridspec
def doplot():
    ion()
    figure(1)
    clf()
    gs = gridspec.GridSpec(3, 2, hspace=0.5, wspace=0.5)
    ax = subplot(gs[0,:])
    cols = ['Amount', 'rental', 'transfer']
    colors = dict(zip(cols, ['r', 'g', 'b']))
    colors['Amount_in'] = 'c'
    colors['Amount_out'] = 'k'
    colors['net'] = 'm'
    d = df.groupby('Date')[cols + ['Amount_in', 'Amount_out']].sum().sort_index()
    d = d.resample('D').sum().fillna(0)
    d['net'] = d['Amount_in'] - d[cols].sum(axis=1)
    for k in cols:
        d[k].plot(ax=ax, drawstyle="steps-post", linewidth=2, label='daily {}'.format(k), alpha=0.5, color=colors[k])
    nn = 30
    dd = d.rolling(window=nn).sum()
    # dd = d.ewm(halflife=nn).mean() * 30
    # dd = d.cumsum() / range(1, d.shape[0]+1) * 30
    for k in ['Amount']:
        dd[k].plot(ax=ax, linewidth=1, label='last {} days {}'.format(nn, k), color=colors[k])
    # a = d.copy()
    # a[:] = 0
    # a.plot()
    title('flows')
    grid()
    # savefig('fig.png')
    legend()
    # axis('tight')
    ax.set_xlabel('')

    ax = subplot(gs[1,:])
    for k in cols + ['net', 'Amount_in', 'Amount_out']:
        d[k].cumsum().plot(ax=ax, drawstyle="steps-post", linewidth=1, label='cumulative {}'.format(k), alpha=1.0, color=colors[k])
    title('cumulative flows')
    legend()
    grid()
    # axis('tight')
    ax.set_xlabel('')

    ax = subplot(gs[2,:])
    # denom = d['Amount_in'].cumsum()
    denom = (d.index - d.index[0]).days.values
    for k in cols + ['net', 'Amount_in', 'Amount_out']:
        temp = d[k].cumsum() / denom
        temp.plot(ax=ax, drawstyle="steps-post", linewidth=1, label='cumulative {}'.format(k), alpha=1.0, color=colors[k])
    title('cumulative flows (daily)')
    ylim(0, 300)
    legend()
    grid()
    # axis('tight')
    ax.set_xlabel('')

    # d['Amount'].groupby(d.index.dayofweek).mean().plot(ax=ax, kind='bar')
    # title('mean weekdays')
    # ax = subplot(gs[2,1])
    # d['Amount'].groupby(d.index.month).mean().plot(ax=ax, kind='bar')
    # title('mean month')
    # axis('tight')
    show()
    return d

def top_things(df):
    a = df.sort_values('Amount', ascending=False)
    a.index = range(a.shape[0])
    return a
    # noninteresting = get_noninteresting_mask(a)
    # return a[~noninteresting]

def top_recent_things(df):
    a = top_things(df)
    # big things last n days
    n = 6 * 30
    start_date = df.Date.max() - datetime.timedelta(days=n)
    i = (a.Date > start_date).values
    return a[i].head(n=30).sort_values('Date', ascending=False)

doplot()
temp = df.iloc[:,:-2]
print("\ntop recent things")
print(top_recent_things(temp))
print("\ntop things all time")
print(top_things(temp).head(n=30))

figure(2)
clf()
gs = gridspec.GridSpec(2, 1, hspace=0.5, wspace=0.5)
ax = subplot(gs[0])
temp = df.groupby('taxyear')[['Amount_in', 'Amount_out']].sum()
temp['net'] = temp.Amount_in - temp.Amount_out
grid()
temp.plot(kind='bar', ax=ax, grid=True)
ax = subplot(gs[1])
t = (temp.T / temp.Amount_in * 100).T
t.plot(kind='bar', ax=ax, grid=True)


