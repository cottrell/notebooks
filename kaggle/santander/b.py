from __future__ import division
import sklearn.neighbors
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
import sklearn.ensemble
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.svm import OneClassSVM
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD

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

    id_test = df_test['ID'].values
    X_test = df_test.drop(['ID'], axis=1).values
    X_train = scipy.sparse.csr_matrix(X_train)
    X_test = scipy.sparse.csr_matrix(X_test)
    X_fit, X_eval, y_fit, y_eval = train_test_split(X_train, y_train, test_size=0.3)

    d = dict()
    for k in ['X_train', 'X_test', 'X_fit', 'X_eval', 'y_train', 'y_fit', 'y_eval', 'id_test']:
        d[k] = locals()[k]
    return d

@bc.cachecalc()
def compute_cosine_distances():
    """ not sure if did this sort of backwards. I think am getting 10 nearest
    train for each test. This will mean some train will not be listed in the
    weights """
    globals().update(get_the_data())
    lsh = sklearn.neighbors.LSHForest(n_estimators=20, n_candidates=100)
    lsh.fit(X_train)
    r = lsh.kneighbors(X_test, return_distance=True, n_neighbors=10)
    return {'r': r}

@bc.cachecalc()
def compute_cosine_distances_2():
    """ other way round """
    globals().update(get_the_data())
    lsh = sklearn.neighbors.LSHForest(n_estimators=20, n_candidates=100)
    lsh.fit(X_test)
    r = lsh.kneighbors(X_train, return_distance=True, n_neighbors=10)
    return {'r': r}

@bc.cachecalc()
def get_test_weights():
    dist, ind = compute_cosine_distances_2()['r']
    w = (1 - np.abs(dist)).mean(axis=1)
    return {'w': w}


@bc.cachecalc()
def get_subsample():
    d = get_data()
    for k in d:
        d[k] = d[k][:10000]
    return d

# get_the_data = get_subsample
get_the_data = get_data

# just do the predict at the same time ...

@bc.cachecalc()
def dofit_xgb(n_estimators=350, max_depth=5, learning_rate=0.03, subsample=0.95, colsample_bytree=0.85, seed=242, early_stopping_rounds=40):
    globals().update(get_the_data())
    clf = xgb.XGBClassifier(missing=np.nan, max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate, nthread=4,
            subsample=subsample, colsample_bytree=colsample_bytree, seed=seed)
    clf.fit(X_fit, y_fit, early_stopping_rounds=early_stopping_rounds, eval_metric="auc", eval_set=[(X_fit, y_fit), (X_eval, y_eval)])
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
def dofit_pyfm(num_iter=1000, num_factors=20):
    globals().update(get_the_data())
    ss = preproc.StandardScaler(with_mean=False) # hmm
    fm = FM(num_factors=num_factors, num_iter=num_iter, verbose=True, task="classification", initial_learning_rate=0.000001, learning_rate_schedule="optimal")
    clf = Pipeline(steps=[('scaler', ss), ('fm', fm)])
    clf.fit(X_fit, y_fit)
    p = clf.predict(X_fit)
    pev = clf.predict(X_eval)
    pte = clf.predict(X_test)
    auc = sklearn.metrics.roc_auc_score(y_fit, p)
    # clf is not pickling properly??? always get 0
    return {'clf': clf, 'y_fit_pred': p, 'auc': auc, 'y_test_pred': pte, 'y_eval_pred': pev}

@bc.cachecalc()
def get_nn_data():
    dd = get_the_data()
    for k in dd:
        if type(dd[k]) is scipy.sparse.csr.csr_matrix:
            dd[k] = dd[k].toarray()
            if len(dd[k].shape) == 1:
                dd[k] = np.atleast_2d(dd[k]).T
    ss = preproc.StandardScaler(with_mean=False) # hmm
    ss.fit(dd['X_fit'])
    for k in dd:
        if k.startswith('X_'):
            dd[k] = ss.transform(dd[k])
    return dd

base_dims = '64,64,64,64'

@bc.cachecalc()
def dofit_nn(dims=base_dims, nb_epoch=100, batch_size=32 * 1024, lr=0.0001, dropout=0.0):
    # 50k fit samples 4k is about 8%
    dd = get_nn_data()
    globals().update(dd)

    model = Sequential()
    dims = [X_fit.shape[1]] + list(map(int, dims.split(',')))
    dropout = dropout
    for i in range(len(dims) - 1):
        model.add(Dense(input_dim=dims[i], output_dim=dims[i+1], init='glorot_uniform'))
        model.add(Activation('tanh'))
        model.add(Dropout(dropout))
    model.add(Dense(input_dim=dims[-1], output_dim=1, init='glorot_uniform'))
    model.add(Activation('sigmoid'))
    sgd = SGD(lr=lr, decay=1e-6, momentum=0.5, nesterov=True)
    model.compile(loss='binary_crossentropy', optimizer=sgd)
    clf = model
    # clf = Pipeline(steps=[('scaling/embedding', ss), ('clf', model)])
    cw = y_fit.shape[0] / y_fit.sum()
    print('training with class_weight={}'.format(cw))
    clf.fit(X_fit, y_fit, nb_epoch=nb_epoch, batch_size=batch_size, validation_data=(X_eval, y_eval), show_accuracy=True, class_weight={0: 1.0, 1: cw})
    # clf.fit(X_fit, y_fit)
    p = clf.predict(X_fit)
    pev = clf.predict(X_eval)
    pte = clf.predict(X_test)
    auc = sklearn.metrics.roc_auc_score(y_fit, p)
    return {'clf': clf, 'y_fit_pred': p, 'auc': auc, 'y_test_pred': pte, 'y_eval_pred': pev}

@bc.cachecalc()
def dofit_nn_01(dims=base_dims, nb_epoch=1000, batch_size=4 * 1024, lr=0.0001, dropout=0.1):
    dd = get_nn_data()
    globals().update(dd)

    # DO NOT TOUCH PARAMS HERE ... make same as above
    dd = dofit_nn(dims=dims, nb_epoch=100, batch_size=32 * 1024, lr=0.0001, dropout=0.0)

    clf = dd['clf']
    sgd = SGD(lr=lr, decay=1e-6, momentum=0.5, nesterov=True)
    clf.compile(loss='binary_crossentropy', optimizer=sgd) # recompile hopefully not clear weights?
    cw = y_fit.shape[0] / y_fit.sum()
    print('training with class_weight={}'.format(cw))
    clf.fit(X_fit, y_fit, nb_epoch=nb_epoch, batch_size=batch_size, validation_data=(X_eval, y_eval), show_accuracy=True, class_weight={0: 1.0, 1: cw})
    # clf.fit(X_fit, y_fit)
    p = clf.predict(X_fit)
    pev = clf.predict(X_eval)
    pte = clf.predict(X_test)
    auc = sklearn.metrics.roc_auc_score(y_fit, p)
    return {'clf': clf, 'y_fit_pred': p, 'auc': auc, 'y_test_pred': pte, 'y_eval_pred': pev}

# don't bother with basic linear model, poor performance
# @bc.cachecalc()
def dofit_logisticregression(penalty='l2', C=1e12, **kwargs):
    globals().update(get_the_data())
    # ss = preproc.StandardScaler(with_mean=False) # hmm
    ss = sklearn.ensemble.RandomTreesEmbedding(n_estimators=1000, min_samples_leaf=20)
    lm = sklearn.linear_model.LogisticRegression(penalty=penalty, C=C, verbose=1)
    clf = Pipeline(steps=[('scaling/embedding', ss), ('clf', lm)])
    clf.fit(X_fit, y_fit)
    p = clf.predict(X_fit)
    pev = clf.predict(X_eval)
    pte = clf.predict(X_test)
    auc = sklearn.metrics.roc_auc_score(y_fit, p)
    return {'clf': clf, 'y_fit_pred': p, 'auc': auc, 'y_test_pred': pte, 'y_eval_pred': pev}

@bc.cachecalc()
def predict():
    globals().update(get_the_data())
    models = {'fm': dofit_pyfm(), 'xgb': dofit_xgb()}
    pred = defaultdict(dict)
    auc = defaultdict(dict)
    for k in models:
        clf = models[k]['clf']
        pred['test'][k] = models[k].get('y_test_pred', clf.predict_proba(X_test)[:,1])
        pred['fit'][k] = models[k].get('y_fit_pred', clf.predict_proba(X_fit)[:,1])
        pred['eval'][k] = models[k].get('y_eval_pred', clf.predict_proba(X_eval)[:,1])
        auc['fit'][k] = sklearn.metrics.roc_auc_score(y_fit, pred['fit'][k])
        auc['eval'][k] = sklearn.metrics.roc_auc_score(y_eval, pred['eval'][k])
        filename = 'submission_b_{}.csv'.format(k)
        y_prob_test = pred['test'][k]
        submission = pd.DataFrame({"ID": id_test, "TARGET": y_prob_test})
        print("writing {}".format(filename))
        submission.to_csv(filename, index=False)
    return {'pred': pred, 'auc': auc}

# # workflow beyond here is dumb
# 
# @bc.cachecalc()
# def get_augmented_data():
#     globals().update(get_the_data())
#     pred = predict()
#     X = X_fit.toarray()
#     Xe = X_eval.toarray()
#     Xt = X_test.toarray()
#     for k in sorted(list(pred['fit'].keys())): # same order
#         X = np.hstack([X, pred['fit'][k][:,0:1]]) # don't need both
#         Xe = np.hstack([Xe, pred['eval'][k][:,0:1]]) # don't need both
#         Xt = np.hstack([Xt, pred['test'][k][:,0:1]]) # don't need both
#     return {'X_fit': X, 'X_eval': Xe, 'X_test': Xt}
# 
# @bc.cachecalc()
# def dofit_ensemble():
#     # TODO: use eval split and use some simpler model that has predict_proba
#     globals().update(get_the_data())
#     globals().update(get_augmented_data())
#     clf = xgb.XGBClassifier(missing=np.nan, max_depth=5, n_estimators=350, learning_rate=0.03, nthread=4, subsample=0.95, colsample_bytree=0.85, seed=4242)
#     clf.fit(X_fit, y_fit, early_stopping_rounds=20, eval_metric="auc", eval_set=[(X_eval, y_eval)])
#     # rc = sklearn.linear_model.RidgeClassifier(alpha=1.0, class_weight=None, copy_X=True,
#     #         fit_intercept=True, max_iter=None, normalize=False, random_state=None, solver='auto', tol=0.001)
#     # rc.fit(X_train, y_train)
#     return {'clf': clf}
# 
# def finalize():
#     id_test = get_the_data()['id_test']
#     globals().update(get_augmented_data())
#     clf = dofit_ensemble()['clf']
#     y_pred = clf.predict(X_train)
#     y_pred_test = clf.predict(X_test)
#     y_prob = clf.predict_proba(X_train)[:,1]
#     y_prob_test = clf.predict_proba(X_test)[:,1] # not sure which one
#     auc_train = roc_auc_score(y_train, y_prob)
#     out = {'clf': clf, 'y_train': y_train, 'y_pred': y_pred, 'y_prob': y_prob, 'y_prod_test': y_prob_test, 'auc_train': auc_train}
#     out['conf'] = confusion_matrix(y_train, y_pred)
#     submission = pd.DataFrame({"ID":id_test, "TARGET":y_prob_test})
#     submission.to_csv("submission_b.csv", index=False)
#     return out



