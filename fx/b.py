"""
data prep and manual feature engineering

feature engineering (widening)
    * diffs
    * rolling std/mean etc
    * date stuff
    * shifts - shifts are covering same space as diffs but we are using trees here

Final step is stacking and treating all as one
"""
import site
import numpy as np
import os
import pandas as pd
_path = os.path.dirname(os.path.abspath(__name__))
site.addsitedir(_path)
import datastore.sources as ds
import functools
import decorator

def _sanity_check(fun, *args, **kwargs):
    df = fun(*args, **kwargs)
    assert len(df.columns) == len(set(df.columns)), 'cols not unique'
    return df

@decorator.decorator(_sanity_check)
def _get_data():
    df = ds.quandl.CURRFX.get_all_cleaned()
    return df

try:
    df
    df = df.sort_index()
except NameError as e:
    df = _get_data()

df_allfeatures = df.copy()

@decorator.decorator(_sanity_check)
def _append_diff_features(df):
    """ expecting columns (blah, blah) """
    temp = [df]
    for i in [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50, 60, 120]:
        df_diff = df.diff(periods=i)
        df_diff.columns = [(x[0] + ' diff {}'.format(i), x[1]) for x in df_diff.columns]
        temp.append(df_diff)
    return pd.concat(temp, axis=1)

@decorator.decorator(_sanity_check)
def _append_rolling_features(df):
    """ TODO """
    return df

@decorator.decorator(_sanity_check)
def _append_date_features(X):
    X['day'] = X.index.day
    X['weekday'] = X.index.weekday
    return X

@decorator.decorator(_sanity_check)
def _append_shift_features(X):
    X = X.copy()
    n_history = 2
    # create shifts as clumsy way of getting last few days as features
    temp = list()
    for i in range(n_history):
        a = X.shift(i).copy()
        a.columns = [(*x, i) for x in a.columns]
        temp.append(a)
    temp = pd.concat(temp, axis=1)
    temp.columns = pd.MultiIndex.from_tuples(temp.columns)
    temp.columns.names = ['type', 'ccyccy', 'shift']
    temp = temp.sort_index(axis=1)
    return temp

df_allfeatures = _append_diff_features(df_allfeatures)
df_allfeatures = _append_date_features(df_allfeatures)
df_allfeatures = _append_rolling_features(df_allfeatures)
df_allfeatures = _append_shift_features(df_allfeatures)

print(df.shape, df_allfeatures.shape)
