import site
import numpy as np
import os
import pandas as pd
_path = os.path.dirname(os.path.abspath(__name__))
site.addsitedir(_path)
import datastore.sources as ds

def _get_data():
    df = ds.quandl.CURRFX.get_all_cleaned()
    return df

def _get_shift_features(X):
    X = X.copy()
    n_history = 1
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

try:
    df
except NameError as e:
    df = _get_data()

df = df.sort_index()
# TODO add more features
temp = [df]
for i in [1, 2, 5, 10, 30]:
    df_diff = df.diff(periods=i)
    df_diff.columns = [(x[0] + ' diff {}'.format(i), x[1]) for x in df_diff.columns]
    temp.append(df_diff)
df_allfeatures = pd.concat(temp, axis=1)

# i.e. [('High (est)', 'GBPUSD'), ('Low (est)', 'GBPUSD'), ('Rate', 'GBPUSD')]
predcols = [x for x in df_allfeatures.columns if x[1] == 'GBPUSD']
predcols_renamed = [(x[0] + ' pred', x[1]) for x in predcols]
ndays_pred = 10 # working days in the future
# confusing but keep the original, unshifted cols there
df_allfeatures[predcols_renamed] = df_allfeatures[predcols].shift(ndays_pred).copy()
df_allfeatures = df_allfeatures.dropna(subset=predcols_renamed)
# y = df_allfeatures[predcols].iloc[:,0] # TODO, need to do these separately
y = df_allfeatures[('Rate diff {} pred'.format(ndays_pred), 'GBPUSD')] # DO NOT FORGET ' pred' suffix !!!!
X_raw = df_allfeatures.copy()
# X_raw = X_raw.drop(predcols_renamed, axis=1)
X_raw = X_raw[predcols]
X = _get_shift_features(X_raw)

# xgboost not like MultiIndex cols
X.columns = ['_'.join(map(str, x)) for x in X.columns]

from sklearn.cross_validation import train_test_split
# no do future vs past
# y_train, X_train, y_test, X_test = train_test_split(y, X, test_size=0.3)
n_test = round(X.shape[0] * 0.3)
ind = np.arange(X.shape[0])
y_train, X_train, y_test, X_test, ind_train, ind_test = y.iloc[:-n_test], X.iloc[:-n_test], y.iloc[-n_test:], X.iloc[-n_test:], ind[:-n_test], ind[-n_test:]

X_fit, X_eval, y_fit, y_eval, ind_fit, ind_eval = train_test_split(X_train, y_train, ind_train, test_size=0.3)

print('shapes', y.shape, X.shape, y_train.shape, X_train.shape, y_test.shape, X_test.shape)

import xgboost as xgb
model = xgb.XGBRegressor(base_score=0.5, colsample_bylevel=1, colsample_bytree=0.5, gamma=0, learning_rate=0.05,
        max_delta_step=0, max_depth=7, min_child_weight=1, missing=None, n_estimators=1000, nthread=-1,
        objective='reg:linear', reg_alpha=0, reg_lambda=1, seed=2, silent=True, subsample=0.3)
model.fit(X_fit, y_fit, eval_set=[(X_fit, y_fit), (X_eval, y_eval), (X_test, y_test)])

y_pred = model.predict(X)

from pylab import *
ion()
figure(1)
clf()
plot(y, y, 'k--', alpha=0.5)
plot(y[ind_fit], y_pred[ind_fit], 'b.', alpha=0.5)
plot(y[ind_eval], y_pred[ind_eval], 'g.', alpha=0.5)
plot(y[ind_test], y_pred[ind_test], 'r.', alpha=0.5)

df_allfeatures['y_pred'] = y_pred
df_allfeatures['y'] = y
figure(2)
clf()
ax = subplot(111)
df_allfeatures.iloc[ind_test][['y', 'y_pred']].plot(ax=ax)


