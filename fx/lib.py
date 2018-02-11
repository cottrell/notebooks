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

_default_diff_periods = [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50, 60, 120]
@decorator.decorator(_sanity_check)
def _append_diff_features(df, periods=_default_diff_periods):
    """ expecting columns (blah, blah) """
    temp = [df]
    for i in periods:
        df_diff = df.diff(periods=i)
        df_diff.columns = [(x[0] + ' diff {}'.format(i), x[1]) for x in df_diff.columns]
        temp.append(df_diff)
    return pd.concat(temp, axis=1)

