from __future__ import division
import sklearn.linear_model
from collections import defaultdict
import sklearn.preprocessing as preproc
from pyfm import pylibfm
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

@bc.cachecalc()
def read_zip():
    d = dict()
    for filename in ['test', 'train']:
        f = filename + '.csv.zip'
        z = zipfile.ZipFile(f).open(filename + '.csv')
        df = pd.read_csv(z)
        print('{} {}'.format(f, df.shape))
        d[filename] = df
    return d

@bc.cachecalc()
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

    X_train = scipy.sparse.csr_matrix(X_train)
    X_test = scipy.sparse.csr_matrix(X_test)
    d = dict(zip(['X_train', 'X_test', 'X_eval', 'y_train', 'y_eval'], [X_train, X_test, X_eval, y_train, y_eval]))
    return d

@bc.cachecalc()
def get_subsample():
    d = get_data()
    for k in d:
        d[k] = d[k][:10000]
    return d

# just do the predict at the same time ... 

@bc.cachecalc()
def dofit_xgb():
    globals().update(get_subsample())
    clf = xgb.XGBClassifier(missing=np.nan, max_depth=5, n_estimators=350, learning_rate=0.03, nthread=4, subsample=0.95, colsample_bytree=0.85, seed=4242)
    clf.fit(X_train, y_train, early_stopping_rounds=20, eval_metric="auc", eval_set=[(X_eval, y_eval)])
    return {'clf': clf}

from sklearn.base import BaseEstimator, TransformerMixin

class ScaleAndSparse(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.scaler = preproc.StandardScaler(with_mean=False) # hmm
    def fit(self, X, y):
        return self.scaler.fit(X)
    def transform(self, X):
        return self.scaler.transform(X)

class FM(pylibfm.FM):
    def predict_proba(self, X):
        p = self.predict(X)
        out = np.empty((len(p), 2), dtype=np.float32)
        out[:,0] = p
        out[:,1] = 1 - p
        return out

@bc.cachecalc()
def dofit_pyfm():
    globals().update(get_subsample())
    ss = preproc.StandardScaler(with_mean=False) # hmm
    fm = FM(num_factors=4, num_iter=10, verbose=True, task="classification", initial_learning_rate=0.00001, learning_rate_schedule="optimal")
    clf = Pipeline(steps=[('scale_and_sparse', ss), ('fm', fm)])
    clf.fit(X_train, y_train)
    return {'clf': clf}

@bc.cachecalc()
def predict():
    globals().update(get_subsample())
    models = {'fm': dofit_pyfm(), 'xgb': dofit_xgb()}
    pred = defaultdict(dict)
    for k in models:
        clf = models[k]['clf']
        pred['test'][k] = clf.predict_proba(X_test)
        pred['train'][k] = clf.predict_proba(X_train)
    return pred

@bc.cachecalc()
def get_augmented_data():
    globals().update(get_subsample())
    pred = predict()
    X = X_train.toarray()
    Xt = X_test.toarray()
    for k in sorted(list(pred['train'].keys())): # same order
        X = np.hstack([X, pred['train'][k]])
        Xt = np.hstack([Xt, pred['test'][k]])
    return {'X_train': X, 'X_test': Xt, 'y_train': y_train}



