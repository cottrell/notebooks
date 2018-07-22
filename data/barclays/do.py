import os
import re
import json
import numpy as np
import glob
import subprocess
import pandas as pd
import shutil
import datetime
import matplotlib.gridspec as gridspec
from pylab import *
pd.options.display.width = 200

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
    files = [glob.glob(os.path.join(_mydir, 'data', x))[-1] for x in ['chequing_20140401_present.csv', 'saver_20140401_present.csv', 'isa_20140401_present.csv']]
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
    df = pd.concat(df)
    df.index = range(df.shape[0])
    return df

def one_hot_to_tags(df, cols, sep='|'):
    s = np.empty(df.shape[0], dtype=object)
    s[:] = ''
    for k in cols:
        i = df[k] != 0
        ii = s != ''
        s[ii] += sep
        s[i] += k
    s = list(map(lambda x: x.rstrip('|'), s)) # ugh, how to np
    return s

abbrev = json.load(open('abbreviations.json'))['data']

def enrich(df):
    # booleans
    d = df.Account.value_counts().index.tolist()
    d = [x.replace('-', '') for x in d]
    def f(x):
        return any([x.startswith(xx) for xx in d])
    df['side'] = np.where(df.Amount > 0, 'in', 'out')
    df['is_b2b'] = df.Memo.apply(f)
    df['is_rental'] = (df.Memo.str.match('^PEACH.*|^VIEW.*|^A A B.*')).values
    df['is_q']  = df.Memo.str.startswith('QI').values
    df['is_transfer']  = df.Memo.str.contains('SIPP').values # out of system but not spend
    t = [x.strip() for x in open('memo_ignore.txt').readlines()]
    df['is_ignorable'] = ((df.Memo == '14CANARY WHARF BRA REM') & (df.Date == '2014-06-10')) | df.Memo.isin(t) # hard code
    df['is_interest'] = df.Memo.str.contains('INTEREST PAID GROSS')
    bool_cols = ['is_b2b', 'is_rental', 'is_q', 'is_transfer', 'is_ignorable', 'is_interest']
    other = ~df[bool_cols].any(axis=1)
    df['is_other_in'] = (df.Amount > 0) & other
    df['is_other_out'] = (df.Amount < 0) & other
    bool_cols = bool_cols + ['is_other_in', 'is_other_out']
    assert df[bool_cols].sum(axis=1).max() == 1, 'not proper partions'
    assert df[bool_cols].sum(axis=1).min() == 1, 'not proper partions'
    df['cat'] = one_hot_to_tags(df, bool_cols)

    # manual Memo stuff for fun
    reg = re.compile('^PEACH .*$')
    reg2 = re.compile('.*PACTC.*')
    reg3 = re.compile('.*WESTJET.*')
    df['msub'] = df.Memo.str[:22].str.strip().str.split('  ').apply(lambda x: x[0]) # .replace(reg, 'PEACH').replace(reg2, 'PACT')
    def do_thing(x, y):
        return df.msub.str.replace(re.compile(x), y)
    df['msub'] = do_thing('^PEACH .*$', 'PEACH')
    df['msub'] = do_thing('.*PACTC.*', 'PACT')
    df['msub'] = do_thing('.*WESTJET.*', 'WESTJET')
    df['msub'] = do_thing('.*EASYJET.*', 'EASYJET')
    df['msub'] = do_thing('.*TESCO.*', 'TESCO')
    df['msub'] = do_thing('.*BOOTS.*', 'BOOTS')
    df['msub'] = do_thing('.*NETFLIX.*', 'NETFLIX')
    i = df.Subcategory == 'CASH'
    df.loc[i, 'msub'] = 'CASH'

    # manglings
    import trainer
    documents, texts = trainer.preproc_docs(df.Memo.unique())
    d = dict(zip(documents, texts))
    df['Memo_'] = df.Memo.map(d)
    # # map to most common (no need)
    # s = df.groupby(['Memo', 'Memo_']).size().sort_values().reset_index().drop_duplicates(['Memo_'], keep='last').set_index('Memo')

    # time cats
    df['month'] = df.Date.apply(lambda x: datetime.datetime(x.year, x.month, 1))
    df['week'] = df.Date.apply(lambda x: '{}-W{}'.format(x.year, x.week))
    df['dayofweek'] = df.Date.apply(lambda x: x.strftime('%w-%a'))
    df['taxyear'] = np.where(df.Date.apply(lambda x: x < datetime.datetime(x.year, 4, 6)).values, df.Date.dt.year - 1, df.Date.dt.year)
    df['taxyear'] = df.taxyear.apply(lambda x: str(x) + '-' + str(x+1)[-2:])
    reg = re.compile('\W*ON\W(\d\d\W[A-Z]{3})\W*')
    df['on_date'] = df.Memo.str.extract(reg)

    return df

try:
    df
except NameError as e:
    df_orig = load_files()
df = enrich(df_orig)
# for the learn bit
filename = 'data.pickle'
print('writing {}'.format(filename))
df.to_pickle(filename)

if 'Number' in df.columns:
    df = df.drop('Number', axis=1)

def get_daily(df):
    d = df.groupby(['Date', 'cat']).Amount.sum().unstack('cat').sort_index().resample('D').sum().fillna(0)
    d.columns = [x.replace('is_', '') for x in d.columns]
    return d

def doplot_flows(df=df):
    df = df.copy()
    ion()
    figure(1)
    clf()
    gs = gridspec.GridSpec(3, 2, hspace=0.5, wspace=0.5)
    ax = subplot(gs[0,:])
    d = get_daily(df)
    # d['net'] = # TODO
    for k in d.columns:
        print(k)
        d[k].plot(ax=ax, drawstyle="steps-post", linewidth=2, label='daily {}'.format(k), alpha=0.5) # , color=colors[k])
    title('flows excluding transfers and b2b')
    grid()
    legend()

    # nn = 30
    # dd = d.rolling(window=nn).sum()
    # ## dd = d.cumsum() / range(1, d.shape[0]+1) * 30
    # for k in dd.columns:
    #     dd[k].plot(ax=ax, linewidth=1, label='last {} days {}'.format(nn, k)) # , color=colors[k])
    #a = d.copy()
    #a[:] = 0
    #a.plot()
    # # axis('tight')
    # ax.set_xlabel('')

    ax = subplot(gs[1,:])
    d['other_out'].plot()
    # for k in cols + ['net', 'amt_in', 'amt_out']:
    #     d[k].cumsum().plot(ax=ax, drawstyle="steps-post", linewidth=1, label='cumulative {}'.format(k), alpha=1.0, color=colors[k])
    # title('cumulative flows')
    # legend()
    # grid()
    # # axis('tight')
    # ax.set_xlabel('')

    # ax = subplot(gs[2,:])
    # # denom = d['amt_in'].cumsum()
    # denom = (d.index - d.index[0]).days.values
    # for k in cols + ['net', 'amt_in', 'amt_out']:
    #     temp = d[k].cumsum() / denom
    #     temp.plot(ax=ax, drawstyle="steps-post", linewidth=1, label='cumulative {}'.format(k), alpha=1.0, color=colors[k])
    # title('cumulative flows (daily)')
    # ylim(0, 300)
    # legend()
    # grid()
    # # axis('tight')
    # ax.set_xlabel('')

    # # d['Amount'].groupby(d.index.dayofweek).mean().plot(ax=ax, kind='bar')
    # # title('mean weekdays')
    # # ax = subplot(gs[2,1])
    # # d['Amount'].groupby(d.index.month).mean().plot(ax=ax, kind='bar')
    # # title('mean month')
    # # axis('tight')
    # show()
    # return d

doplot_flows()

# savefig(os.path.join(_mydir, 'figure_1.png'))

# def top_things(df):
#     a = df.sort_values('Amount', ascending=False)
#     a.index = range(a.shape[0])
#     return a
#     # noninteresting = get_noninteresting_mask(a)
#     # return a[~noninteresting]

# def top_recent_things(df):
#     a = top_things(df)
#     # big things last n days
#     n = 6 * 30
#     start_date = df.Date.max() - datetime.timedelta(days=n)
#     i = (a.Date > start_date).values
#     return a[i].head(n=30).sort_values('Date', ascending=False)

_cols = ['Date', 'Account', 'Amount', 'Subcategory', 'Memo']
# temp = df.iloc[:,:-2][_cols]
# print("\ntop recent things")
# print(top_recent_things(temp))
# print("\ntop things all time")
# print(top_things(temp).head(n=30))
# 
# figure(2)
# clf()
# gs = gridspec.GridSpec(2, 1, hspace=0.5, wspace=0.5)
# ax = subplot(gs[0])
# temp = df.groupby('taxyear')[['amt_in', 'amt_out']].sum()
# temp['net'] = temp.amt_in - temp.amt_out
# grid()
# temp.plot(kind='bar', ax=ax, grid=True)
# ax = subplot(gs[1])
# t = (temp.T / temp.amt_in * 100).T
# t.plot(kind='bar', ax=ax, grid=True)
# savefig(os.path.join(_mydir, 'figure_2.png'))


