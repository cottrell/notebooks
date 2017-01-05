import site
import numpy as np
import os
import pandas as pd
_path = os.path.dirname(os.path.abspath(__name__))
site.addsitedir(_path)
import datastore.sources as ds

YTYPE = 'linear'
# YTYPE = 'sign'
ndays_pred = 40 # working days in the future, 20 is a month?
# CCYCCY = 'GBPUSD'
# CCYCCY = 'CADUSD'
# CCYCCY = 'CHFUSD'
CCYCCY = 'CNYUSD' # interesting
n_features = 12 
n_history = 1

def _get_data():
    df = ds.quandl.CURRFX.get_all_cleaned()
    return df

def _get_shift_features(X):
    X = X.copy()
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

def _get_date_features_from_index(X):
    X['day'] = X.index.day
    X['weekday'] = X.index.weekday
    return X

try:
    df
except NameError as e:
    df = _get_data()

df = df.sort_index()
# TODO add more features
temp = [df]
for i in [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50, 60, 120]:
    df_diff = df.diff(periods=i)
    df_diff.columns = [(x[0] + ' diff {}'.format(i), x[1]) for x in df_diff.columns]
    temp.append(df_diff)
df_allfeatures = pd.concat(temp, axis=1)

# i.e. [('High (est)', 'GBPUSD'), ('Low (est)', 'GBPUSD'), ('Rate', 'GBPUSD')]
predcols = [x for x in df_allfeatures.columns if x[1] == CCYCCY]
predcols_renamed = [(x[0] + ' pred', x[1]) for x in predcols]
# confusing but keep the original, unshifted cols there
df_allfeatures[predcols_renamed] = df_allfeatures[predcols].shift(ndays_pred).copy()
df_allfeatures = df_allfeatures.dropna(subset=predcols_renamed)
# y = df_allfeatures[predcols].iloc[:,0] # TODO, need to do these separately
y_colname = ('Rate diff {} pred'.format(ndays_pred), CCYCCY)
y = df_allfeatures[y_colname] # DO NOT FORGET ' pred' suffix !!!!
if YTYPE == 'sign':
    y = y > 0
X_raw = df_allfeatures.copy()
# X_raw = X_raw.drop(predcols_renamed, axis=1)
X_raw = X_raw[predcols]
X = _get_shift_features(X_raw)
X = _get_date_features_from_index(X)

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

# feature importance/selection
import sklearn.ensemble as se
if YTYPE == 'linear':
    etr = se.ExtraTreesRegressor(bootstrap=True, criterion='mse', max_depth=3,
           max_features='auto', max_leaf_nodes=None, min_samples_leaf=5, min_samples_split=2, min_weight_fraction_leaf=0.0,
           n_estimators=100, n_jobs=1, oob_score=True, random_state=None, verbose=0, warm_start=False)
    etr.fit(X_fit.fillna(method='ffill').fillna(0), y_fit)
elif YTYPE == 'sign':
    etr = se.ExtraTreesClassifier(bootstrap=True, class_weight=None, criterion='gini', max_depth=3,
            max_features='auto', max_leaf_nodes=None, min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=-1, oob_score=True, random_state=None,
            verbose=1, warm_start=False)
    etr.fit(X_fit.fillna(method='ffill').fillna(0), y_fit)

s = pd.Series(etr.feature_importances_, index=X_fit.columns)
s.sort(ascending=True)

def doplotA(y, y_pred):
    plot(y, y, 'k--', alpha=0.5)
    plot(y[ind_fit], y_pred[ind_fit], 'b.', alpha=0.5)
    plot(y[ind_eval], y_pred[ind_eval], 'g.', alpha=0.5)
    plot(y[ind_test], y_pred[ind_test], 'r.', alpha=0.5)

from pylab import *
ion()
figure(3)
clf()
ax = subplot(122)
s.head(n=20).plot(ax=ax, kind='barh')
figure(4)
clf()
if YTYPE == 'linear':
    y_pred = etr.predict(X.fillna(method='ffill').fillna(0)) # TODO handle nan
    doplotA(y, y_pred)
    title('Extra Trees Pred for feature selection')

# # really need to get this in a proper pipeline
# i_features = np.argsort(etr.feature_importances_) < n_features
# reduce_features = lambda x: x.iloc[:,i_features]
# X_fit = reduce_features(X_fit)
# X_test = reduce_features(X_test)
# X_train = reduce_features(X_train)
# X_eval = reduce_features(X_eval)
# X = reduce_features(X)
# 
# import xgboost as xgb
# if YTYPE == 'linear':
#     model = xgb.XGBRegressor(base_score=0.5, colsample_bylevel=1, colsample_bytree=0.5, gamma=0, learning_rate=0.1,
#             max_delta_step=0, max_depth=3, min_child_weight=1, missing=None, n_estimators=100, nthread=-1,
#             objective='reg:linear', reg_alpha=0, reg_lambda=1, seed=2, silent=True, subsample=0.3)
#     model.fit(X_fit, y_fit, eval_set=[(X_fit, y_fit), (X_eval, y_eval), (X_test, y_test)])
# elif YTYPE == 'sign':
#     model = xgb.XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=0.5, gamma=0, learning_rate=0.01,
#             max_delta_step=0, max_depth=3, min_child_weight=1, missing=None, n_estimators=1000, nthread=-1,
#             reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=0, silent=True, subsample=1)
#     model.fit(X_fit, y_fit, eval_set=[(X_fit, y_fit), (X_eval, y_eval), (X_test, y_test)], eval_metric='auc')
# 
# y_pred = model.predict(X)
# 
# figure(1)
# clf()
# if YTYPE == 'linear':
#     doplotA(y, y_pred)
#     title('y vs y_pred {} (ndays = {})'.format(y_colname, ndays_pred))
# 
#     df_allfeatures['y_pred'] = y_pred
#     df_allfeatures['y'] = y
# figure(2)
# clf()
# if YTYPE == 'linear':
#     ax = subplot(111)
#     df_allfeatures.iloc[ind_test][['y', 'y_pred']].plot(ax=ax)
#     title('y vs y_pred on test set\n{} (ndays = {})'.format(y_colname, ndays_pred))
# 
# 
# 
