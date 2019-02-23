from pylab import *
import pickle
import bc
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.svm import OneClassSVM
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import functools

def print_name_if_run(fun):
    @functools.wraps(fun)
    def inner(*args, **kwargs):
        print('running: {}'.format(fun.__name__))
        fun(*args, *kwargs)
    return inner

def extreme_stacked_format():
    from dataprep import df_train, df_test
    df_train = d['train']
    df_test = d['test']
    d = df_train[xcols].stack()
    d = d[d!=0]
    y = df_train[[ycol]].stack()
    d = pd.concat([d, y])
    del y
    d = d.reset_index()
    d.columns = ['ID', 'col', 'value']
    d = d.sort_values(by=['ID', 'col'])
    for k in ['ID', 'col']:
        d[k] = d[k].astype('category')
    return d

def get_data():
    try:
        d = bc.from_carrays('extreme_stacked_format.bcolz')
        print("read from extreme_stacked_format.bcolz")
    except Exception as e:
        print(e)
        print('re-processing from original data')
        d = extreme_stacked_format()
        bc.to_carrays(d, 'extreme_stacked_format.bcolz')
    return d

def get_XY():
    d = get_data()
    m = d.shape[0]
    n = 2
    X = np.empty((m, n), dtype=np.float32)
    X[:,0], X[:,1] = d['ID'].cat.codes.values, d['col'].cat.codes.values
    y = d['value'].values
    y = np.atleast_2d(y).T
    return X, y

def get_train_test_split():
    X_train, y_train = get_XY()
    X_fit, X_eval, y_fit, y_eval = train_test_split(X_train, y_train, test_size=0.3)
    return X_fit, X_eval, y_fit, y_eval

try:
    X_fit
except NameError as e:
    X_fit, X_eval, y_fit, y_eval = get_train_test_split()

def get_model():
    
    m = X_fit.shape[1]
    n = y_fit.shape[1]
    
    dims = [64] * 32
    model = Sequential()
    model.add(Dense(input_dim=m, output_dim=dims[0], init='glorot_uniform'))
    model.add(Activation('sigmoid')) # relu not exist?
    for i in range(len(dims)-1):
        # model.add(Dropout(dropout))
        model.add(Dense(input_dim=dims[i], output_dim=dims[i+1], init='glorot_uniform'))
        model.add(Activation('sigmoid'))
    model.add(Dense(input_dim=dims[-1], output_dim=n, init='glorot_uniform'))
    model.add(Activation('sigmoid'))
     
    sgd = SGD(lr=0.1, decay=1e-4, momentum=0.9, nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd)
    # model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    # model.compile(loss='binary_crossentropy', optimizer=sgd)
    return model

try:
    model
    asdf
except NameError as e:
    model = get_model()

def fit_model():
    return model.fit(X_fit, y_fit, nb_epoch=100, batch_size=2 ** 15, validation_data=(X_eval, y_eval), show_accuracy=True)

try:
    out = pickle.load(open('model_callback.pkl', 'rb'))
    model = pickle.load(open('model_trained.pkl', 'rb'))
except Exception as e:
    out = fit_model()
    pickle.dump(open('model_callback.pkl', 'wb'))
    pickle.dump(open('model_trained.pkl', 'wb'))

# h = pd.DataFrame(out.history)
# h[['loss', 'val_loss']].plot(logy=True)
# grid()
# 
# yp = model.predict(X_fit)
# ypt = model.predict(X_eval)

