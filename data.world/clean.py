import pandas as pd
import numpy as np
def genkey():
    fin = open('key.txt')
    d = fin.readlines()
    d = [x.strip() for x in d if x.strip()]
    d = [x for x in d if not x.startswith('#')]
    d = [x for x in d if not x.endswith('?')]
    # d = [x.split(':')[0] for x in d]

    def f(x):
        if ':' in x:
            x = x.split(':')[0] + ':'
        if '=' in x:
            x = [xx.strip() for xx in x.split('=')]
            assert len(x)==2
            try:
                int(x[0])
            except ValueError:
                int(x[1])
                x = [x[1], x[0]]
            x = '='.join(x)
        return x

    d = [f(x) for x in d]

    out = dict()
    k = None
    temp = dict()
    for x in d:
        if ':' in x:
            if k is not None:
                out[k] = temp
                temp = dict()
            k = x.split(':')[0]
        if '=' in x:
            xx = x.split('=')
            temp[xx[0]] = xx[1]

    dd = {k.replace(' ', '_'): {int(kk): vv for kk, vv in v.items()} for k, v in out.items()}
    import json
    json.dump(dd, open('key.json', 'w'))

def prep():
    df = pd.read_csv('Speed Dating Data.csv', encoding='latin-1')
    import json
    dk = json.load(open('key.json'))
    dk = {k: {int(kk): vv for kk, vv in v.items()} for k, v in dk.items()}

    c = list(dk.keys())
    for k, v in dk.items():
        if len(v) > 0:
            print('mapping {}'.format(k))
            df[k] = df[k].map(lambda x: v[x] if not np.isnan(x) else x)
    df['race_o'] = df['race_o'].map(dk['race'])
    df = df[c]

    df = df.dropna(subset=['iid', 'pid'], how='any').copy()
    for k in ['iid', 'pid']:
        df[k] = df[k].astype(int)

    for k in ['idg', 'iid', 'round', 'partner', 'position']:
        df[k] = df[k].astype('category')
    for k in ['order']:
        df[k] = df[k].astype('float')

    for k in df:
        if df[k].dtype.name == 'object':
            df[k] = df[k].astype('category')
        if df[k].dtype.name.startswith('int'):
            print(k, df[k].min(), df[k].max())

    # better be one
    assert df.groupby(['iid', 'pid']).size().max() == 1

    i = df.gender == 'Female'
    a = df[i]
    b = df[~i].copy()
    assert a.shape[0] + b.shape[0] == df.shape[0]
    c = ['iid', 'pid']
    a = a.set_index(c)
    x = b['pid'].copy()
    b['pid'] = b['iid'].copy()
    b['iid'] = x
    b = b.set_index(c)
    b.columns = ['{}_male'.format(x) for x in b.columns]
    a.columns = ['{}_female'.format(x) for x in a.columns]
    d = pd.concat([a, b], axis=1)
    assert all(d.match_female == d.match_male)
    d = d.rename(columns={'dec_o_female': 'dec_male', 'dec_o_male': 'dec_female'})
    d = d.drop(['match_male'], axis=1)
    import mylib.tools as tools
    tools.convert_to_categorical_inplace(d)
    return d, df


