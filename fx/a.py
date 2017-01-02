import site
import os
import pandas as pd
_path = os.path.dirname(os.path.abspath(__name__))
site.addsitedir(_path)
import datastore.sources as ds

def _get_data():
    df = ds.quandl.CURRFX.get_all_cleaned()
    return df

try:
    df
except NameError as e:
    df = _get_data()

predcol = 'GBPUSD'
ndays_pred = 3 # ten working days in the future
y = df.xs(predcol, level=1, axis=1).shift(ndays_pred)

y = y.iloc[ndays_pred:].copy()
X = df.iloc[ndays_pred:].copy()

def _get_shift_features(X):
    X = X.copy()
    n_history = 10
    # create shifts as clumsy way of getting last few days as features
    temp = list()
    for i in range(n_history):
        a = X.shift(i)
        a.columns = [(*x, i) for x in a.columns]
        temp.append(a)
    temp = pd.concat(temp, axis=1)
    temp.columns = pd.MultiIndex.from_tuples(temp.columns)
    temp.columns.names = ['type', 'ccyccy', 'shift']
    temp = temp.sort_index(axis=1)
    return temp


