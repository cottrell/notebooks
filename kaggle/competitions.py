import pandas as pd
import glob
import os
import pickle
# >>> from sklearn.externals import joblib
# >>> joblib.dump(clf, 'filename.joblib')
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
import sklearn.metrics
from mylib import attributedict_from_locals
from mylib.cache import SimpleNode

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
    xcols = ['r', 'days_remaining']
    df_ = df[df.r > 0]
    y = df_[ycols]
    X = df_[xcols].astype(float) # just in case this matters
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, random_state=1)
    return attributedict_from_locals('df,X_train,X_test,y_train,y_test')

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
           per_run_time_limit=360, resampling_strategy='holdout',
           resampling_strategy_arguments=None, seed=1, shared_mode=False,
           smac_scenario_args=None, time_left_for_this_task=3600,
           tmp_folder=None)
    model.fit(l.X_train.values, l.y_train.values.squeeze())
    # y_hat = automl.predict(l.X_test)
    # print("Accuracy score", sklearn.metrics.accuracy_score(l.y_test, y_hat))
    return attributedict_from_locals('model')




def do_plots(df=None):
    if df is None:
        l = get_data()
        df = l['df']
    figure(1)
    clf()
    ax = subplot(121)
    grid()
    sns.scatterplot(x='r', y='teamCount', hue='is_active', data=df, alpha=0.5, ax=ax)
    ax.set_xscale('log')
    ax = subplot(122)
    sns.scatterplot(x='days_remaining', y='teamCount', hue='is_active', data=df, alpha=0.5, ax=ax)
    grid()

    fig = plt.figure(2)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df.logr, df.days_remaining, df.teamCount) # , c=c, marker=m)
    ax.set_xlabel('log(r)')
    ax.set_ylabel('days remaining')
    ax.set_zlabel('team count')
    plt.show()

if __name__ == '__main__':
    l = get_data()
else:
    l = get_data()
    df_orig = l['df']
    df = df_orig[df_orig.r > 0]
    # do_plots(df=df)
