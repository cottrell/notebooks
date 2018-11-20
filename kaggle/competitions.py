import pandas as pd
import glob
import os
import pickle
import datetime
import re
from pylab import *
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import numpy as np
# import autosklearn.classification
from autosklearn.regression import AutoSklearnRegressor
import sklearn.model_selection
import sklearn.datasets
from sklearn.svm import LinearSVR, SVR
from tpot import TPOTRegressor
import sklearn.metrics
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import QuantileTransformer
from sklearn.gaussian_process import GaussianProcessRegressor, kernels
import autokeras as ak

from mylib import attributedict_from_locals
from mylib.cache import SimpleNode # just use joblib.Memory.cache
import joblib
_mydir = os.path.dirname(__file__)
cachedir = os.path.join(_mydir, 'joblib_cache')
memory = joblib.Memory(cachedir, verbose=1)

_mydir = os.path.dirname(__file__)
ion()

def get_data():
    df = pd.read_csv('kaggle_competitions.csv', parse_dates=['deadline'])
    def f(x):
        if '$' in x:
            return float(x.lstrip('$').replace(',', ''))
        return 0
    df['r'] = df.reward.apply(f) / 1000

    df['is_active'] = df.deadline > datetime.datetime.today()
    df['year'] = df.deadline.dt.year
    df['month'] = df.deadline.dt.month
    df['days_remaining'] = (df.deadline - datetime.datetime.today()).dt.days
    df['logr'] = np.log10(df.r)
    ycols = ['teamCount']
    xcols = ['logr', 'days_remaining']
    df_ = df[df.r > 0]
    # ugh better to label a column as train test
    y = df_[ycols]
    X = df_[xcols].astype(float) # just in case this matters
    data = df_[xcols + ycols].rename(columns={ycols[0]: 'target'})
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, random_state=1)
    return attributedict_from_locals('df,data,X_train,X_test,y_train,y_test')

@SimpleNode
def train_autokeras(l=None):
    if l is None:
        l = get_data()
    dirname = os.path.join(_mydir, 'autokeras')
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    model = ak.ImageRegressor(path=dirname)
    # TODO fix this shape ...
    model.fit(np.atleast_3d(l.X_train.values), l.y_train.values.squeeze())
    return attributedict_from_locals('model')

@SimpleNode
def train_gpr(l=None):
    # basic no tuning
    if l is None:
        l = get_data()
    model = GaussianProcessRegressor(alpha=1.8, copy_X_train=True, kernel=kernels.RBF(4.85 * np.array([4, 3000])),
             n_restarts_optimizer=0, normalize_y=False,
             optimizer='fmin_l_bfgs_b', random_state=None)
    # model = TransformedTargetRegressor(regressor=model, transformer=QuantileTransformer(output_distribution='normal'))
    model.fit(l.X_train.values, l.y_train.values.squeeze())
    return attributedict_from_locals('model')

@SimpleNode
def train_svm(l=None):
    # basic no tuning
    if l is None:
        l = get_data()
    model = SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
        kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
    model = TransformedTargetRegressor(regressor=model, transformer=QuantileTransformer(output_distribution='normal'))
    # model = LinearSVR(C=1.0, dual=True, epsilon=0.0, fit_intercept=True,
    #     intercept_scaling=1.0, loss='epsilon_insensitive', max_iter=1000,
    #     random_state=None, tol=0.0001, verbose=0)
    model.fit(l.X_train.values, l.y_train.values.squeeze())
    return attributedict_from_locals('model')

@SimpleNode
def train_tpot(l=None):
    # can also do directly from the command line
    if l is None:
        l = get_data()
    model = TPOTRegressor(config_dict=None, crossover_rate=0.1, cv=5,
        disable_update_check=False, early_stop=None, generations=100,
        max_eval_time_mins=5, max_time_mins=None, memory=os.path.join(_mydir, 'tpot_cache'),
        mutation_rate=0.9, n_jobs=1, offspring_size=None,
        periodic_checkpoint_folder='tpot_periodic_checkpoint', population_size=100,
        random_state=None, scoring=None, subsample=1.0, use_dask=False,
        verbosity=1, warm_start=False)
    model.fit(l.X_train.copy(), l.y_train.copy())
    # to be safe:
    model.export('tpot_exported_pipeline.py')
    return attributedict_from_locals('model')

@SimpleNode
def train_autosklearn(l=None):
    if l is None:
        l = get_data()
    ensemble_size = 1 # 50 ... 1 for vanilla
    initial_configurations_via_metalearning = 0 # 25 ... 0 for vanilla
    model = AutoSklearnRegressor(delete_output_folder_after_terminate=True,
           delete_tmp_folder_after_terminate=True,
           disable_evaluator_output=False, ensemble_nbest=50,
           ensemble_size=ensemble_size, exclude_estimators=None,
           exclude_preprocessors=None, get_smac_object_callback=None,
           include_estimators=None, include_preprocessors=None,
           initial_configurations_via_metalearning=initial_configurations_via_metalearning, logging_config=None,
           ml_memory_limit=3072, output_folder=None,
           per_run_time_limit=360,
           resampling_strategy='cv',
           resampling_strategy_arguments={'folds': 5},
           # resampling_strategy='holdout',
           # resampling_strategy_arguments=None,
           seed=1, shared_mode=False,
           smac_scenario_args=None, time_left_for_this_task=3600,
           tmp_folder=None)
    model.fit(l.X_train.values.copy(), l.y_train.values.squeeze().copy())
    model.refit(l.X_train.values.copy(), l.y_train.values.squeeze().copy())
    print(model.show_models())
    return attributedict_from_locals('model')

def plot_predict(model):
    # model = train_autosklearn.get_latest().model
    d = get_data()
    yh_train = model.predict(d.X_train).squeeze()
    yh_test = model.predict(d.X_test).squeeze()
    d.y_train = d.y_train.squeeze()
    d.y_test = d.y_test.squeeze()

    figure(1)
    clf()
    show()
    plot(d.y_train, d.y_train, 'k-', alpha=0.5, label=None)
    plot(d.y_train, yh_train, 'bo', alpha=0.5, label='train')
    plot(d.y_test, yh_test, 'ro', alpha=0.5, label='test')
    legend()

    n = 50
    mm = 40
    df = d.df; df = df[df.r > 0]
    logr = linspace(-1, df.logr.max(), mm)
    days_remaining = linspace(df.days_remaining.min(), df.days_remaining.max(), n)
    X, Y = meshgrid(logr, days_remaining)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    Z = model.predict(xy).reshape(X.shape)

    fig = plt.figure(2)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, linewidth=1, alpha=0.5)
    ax.set_xlabel('log(r)')
    ax.set_ylabel('days remaining')
    ax.set_zlabel('team count')
    plt.show()

    return attributedict_from_locals() # locals()

def do_plots(df=None):
    if df is None:
        l = get_data()
        df = l['df']
    figure(2)
    clf()
    ax = subplot(121)
    grid()
    sns.scatterplot(x='r', y='teamCount', hue='is_active', data=df, alpha=0.5, ax=ax)
    ax.set_xscale('log')
    ax = subplot(122)
    sns.scatterplot(x='days_remaining', y='teamCount', hue='is_active', data=df, alpha=0.5, ax=ax)
    grid()

    fig = figure(3)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df.logr, df.days_remaining, df.teamCount) # , c=c, marker=m)
    ax.set_xlabel('log(r)')
    ax.set_ylabel('days remaining')
    ax.set_zlabel('team count')
    show()

    figure(5)
    clf()
    subplot(121)
    plot(l['X_train'].logr, l['y_train'].teamCount, 'bo', alpha=0.5)
    plot(l['X_test'].logr, l['y_test'].teamCount, 'ro', alpha=0.5)
    subplot(122)
    plot(l['X_train'].days_remaining, l['y_train'].teamCount, 'bo', alpha=0.5)
    plot(l['X_test'].days_remaining, l['y_test'].teamCount, 'ro', alpha=0.5)

if __name__ == '__main__':
    l = get_data()
else:
    l = get_data()
    # globals().update(l)
    df_orig = l['df']
    df = df_orig[df_orig.r > 0]
    # do_plots(df=df)
    # l = train_svm()
    # plot_predict(l.model)
