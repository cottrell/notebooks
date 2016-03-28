from __future__ import division
from fastFM import als, sgd
import scipy.sparse
import zipfile
import bc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.svm import OneClassSVM

def read_zip():
    d = dict()
    for filename in ['test', 'train']:
        f = filename + '.csv.zip'
        z = zipfile.ZipFile(f).open(filename + '.csv')
        df = pd.read_csv(z)
        print('{} {}'.format(f, df.shape))
        d[filename] = df
    return d

def get_data():
    d = read_zip()
    df_train = d['train']
    df_test = d['test']

    # remove constant columns
    remove = []
    for col in df_train.columns:
        if df_train[col].std() == 0:
            remove.append(col)

    df_train.drop(remove, axis=1, inplace=True)
    df_test.drop(remove, axis=1, inplace=True)

    # remove duplicated columns
    remove = []
    # WHAT IS PERF LIKE WITHOUT REMOVE?
    c = df_train.columns
    for i in range(len(c)-1):
        v = df_train[c[i]].values
        for j in range(i+1,len(c)):
            if np.array_equal(v,df_train[c[j]].values):
                remove.append(c[j])

    df_train.drop(remove, axis=1, inplace=True)
    df_test.drop(remove, axis=1, inplace=True)

    y_train = df_train['TARGET'].values
    X_train = df_train.drop(['ID','TARGET'], axis=1).values

    id_test = df_test['ID']
    X_test = df_test.drop(['ID'], axis=1).values
    X_fit, X_eval, y_fit, y_eval = train_test_split(X_train, y_train, test_size=0.3)
    d = dict(zip(['X_train', 'X_test', 'X_eval', 'y_train', 'y_eval'], [X_train, X_test, X_eval, y_train, y_eval]))
    return d

try:
    d = bc.from_dict_of_blocks('data')
except Exception as e:
    print(e)
    d = get_data()
    bc.to_dict_of_blocks(d, 'data')
    d = bc.from_dict_of_blocks('data')

# pull into numpy arrays
for k in d:
    d[k] = d[k][:].astype(np.float64)
globals().update(d)

import sklearn.preprocessing as preproc
scaler = preproc.StandardScaler(with_mean=False) # hmm
scaler.fit(X_train)

def transx(X):
    return scipy.sparse.csr_matrix(scaler.transform(X))
def transy(y):
    return np.where(y==0.0, -1.0, y)
def transy_inv(y):
    return np.where(y==-1.0, 0.0, y)

def patched_factory(klass, *args, **kwargs):
    fm = klass(*args, **kwargs)
    fm._fit_old = fm.fit
    fm.fit = lambda X_train, y_train: fm._fit_old(transx(X_train), transy(y_train))
    fm.fit(X_train, y_train)
    fm._predict_old = fm.predict
    fm.predict = lambda x: transy_inv(fm._predict_old(transx(x)))
    fm._predict_proba_old = fm.predict_proba
    fm.predict_proba = lambda x: transy_inv(fm._predict_proba_old(transx(x)))
    return fm

def dofit_fastfm():
    """ unstable/not working for predict_proba ... not sure if worth it to dig through problems """
    # method does not work with some combination of arguments (ls_reg=None for example)
    fm = patched_factory(sgd.FMClassification, n_iter=1000, init_stdev=0.1, l2_reg_w=0, l2_reg_V=0, rank=2, step_size=0.1)
    fm.fit(X_train, y_train)
    return fm

def dofit_xgb():
    # classifier
    clf = xgb.XGBClassifier(missing=np.nan, max_depth=5, n_estimators=350, learning_rate=0.03, nthread=4, subsample=0.95, colsample_bytree=0.85, seed=4242)
    # fitting
    clf.fit(X_train, y_train, early_stopping_rounds=20, eval_metric="auc", eval_set=[(X_eval, y_eval)])
    # print('Overall AUC:', roc_auc_score(y_train, clf.predict_proba(X_train)[:,1]))
    # # predicting
    # y_pred = clf.predict_proba(X_test)[:,1]
    # submission = pd.DataFrame({"ID":id_test, "TARGET":y_pred})
    # submission.to_csv("submission.csv", index=False)
    # print('Completed!')
    return clf

trained_models = dict()
# trained_models['fm'] = dofit_fastfm()
# fm = trained_models['fm']
# trained_models['xgb'] = dofit_xgb()

# for k, clf in trained_models.items():
#     # print('Overall AUC:', roc_auc_score(y_train, clf.predict_proba(X_train)[:,1]))
#     # y_pred = clf.predict_proba(X_test)[:,1]
