"""
main deal is to learn to use tpot and things like that
"""
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
import tpot
tpot._RAISE_CONFIG_DICT_ERRORS = True
from tpot import TPOTRegressor
import sklearn.metrics
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import QuantileTransformer, MinMaxScaler
from sklearn.pipeline import FeatureUnion, Pipeline
import sklearn.compose as compose
from sklearn.gaussian_process import GaussianProcessRegressor, kernels
import autokeras as ak

from mylib import attributedict_from_locals
from mylib.cache import SimpleNode # just use joblib.Memory.cache
import joblib

import tensorflow as tf
# tf.enable_eager_execution() # breaks some patterns see below
from tensorflow_probability import distributions as tfd
from tensorflow_probability import positive_semidefinite_kernels as tfk

def reset_session():
  """Creates a new global, interactive session in Graph-mode."""
  global sess
  try:
    tf.reset_default_graph()
    sess.close()
  except:
    pass
  sess = tf.InteractiveSession()

reset_session()

_mydir = os.path.dirname(__file__)
cachedir = os.path.join(_mydir, 'joblib_cache')
memory = joblib.Memory(cachedir, verbose=1)
ion()

# @SimpleNode
def train_gpr(l=None):
    # basic no tuning. sklearn gp is not great for this.
    if l is None:
        l = get_data()
    model = GaussianProcessRegressor(
        alpha=1.8,
        copy_X_train=True,
        # kernel=kernels.RBF(4.85 * np.array([4, 3000])),
        # kernel=kernels.RBF([1, 1]),
        n_restarts_optimizer=10,
        normalize_y=True,
        optimizer='fmin_l_bfgs_b',
        random_state=None
        )
    model = TransformedTargetRegressor(regressor=model, transformer=QuantileTransformer(output_distribution='normal'))
    steps = [('copulize_x', QuantileTransformer(output_distribution='uniform')),
             ('gpr', model)]
    model = Pipeline(steps)
    model.fit(l.X_train.values, l.y_train.values.squeeze())
    return attributedict_from_locals('model')

def train_gpr_tfp(l=None):
    if l is None:
        l = get_data()
    amplitude = (np.finfo(np.float64).tiny + tf.nn.softplus(tf.Variable(initial_value=1.,
                                        name='amplitude',
                                        dtype=np.float64)))
    length_scale = (np.finfo(np.float64).tiny + tf.nn.softplus(tf.Variable(initial_value=1.,
                                           name='length_scale',
                                           dtype=np.float64)))
    observation_noise_variance = (np.finfo(np.float64).tiny + tf.nn.softplus(tf.Variable(initial_value=1e-6,
                               name='observation_noise_variance',
                               dtype=np.float64)))
    kernel = tfk.ExponentiatedQuadratic(amplitude, length_scale)
    model_train = tfd.GaussianProcess(
        kernel=kernel,
        index_points=l.X_train.values,
        observation_noise_variance=observation_noise_variance)
    log_likelihood = model_train.log_prob(l.y_train.values.squeeze())
    optimizer = tf.train.AdamOptimizer(learning_rate=.01)
    train_op = optimizer.minimize(-log_likelihood)

    # training
    num_iters = 2000
    # Store the likelihood values during training, so we can plot the progress
    lls_ = np.zeros(num_iters, np.float64)
    sess.run(tf.global_variables_initializer())
    for i in range(num_iters):
      _, lls_[i] = sess.run([train_op, log_likelihood])
    [amplitude_,
     length_scale_,
     observation_noise_variance_] = sess.run([
        amplitude,
        length_scale,
        observation_noise_variance])
    print('Trained parameters:'.format(amplitude_))
    print('amplitude: {}'.format(amplitude_))
    print('length_scale: {}'.format(length_scale_))
    print('observation_noise_variance: {}'.format(observation_noise_variance_))

    # Plot the loss evolution
    plt.figure(1, figsize=(12, 4))
    plt.plot(lls_)
    plt.xlabel("Training iteration")
    plt.ylabel("Log marginal likelihood")
    plt.show()

    # tfp is a bit weird ... you need to create another model for inference ... it isn't a model really it is the thing that represents the distribution
    # notice that we now provide more arguments
    model_infer = tfd.GaussianProcessRegressionModel(
        kernel=kernel,  # Reuse the same kernel instance, with the same params
        index_points=l.X_test.values,
        observation_index_points=l.X_train.values,
        observations=l.y_train.values.squeeze(),
        observation_noise_variance=observation_noise_variance,
        predictive_noise_variance=tf.constant(0., dtype=np.float64))

    ## make a .predict wrapper. It is strange that model_infer does not explicitly have knowledge of the observations yet those are needed for inference.
    # test:
    num_samples = 50
    samples = model_infer.sample(num_samples)

    return attributedict_from_locals('model_train,model_infer,samples')


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
    df_ = df[df.r > 0].copy()
    df_['r'] = np.log10(df_['r'])
    ycols = ['teamCount']
    xcols = ['r', 'days_remaining']
    # ugh better to label a column as train test
    y = df_[ycols].astype(float) # tf does not like it when int
    X = df_[xcols].astype(float) # just in case this matters

    # ##########################
    # # this is cheating the cv! learn to put these in tpot ...
    # X = QuantileTransformer().fit_transform(X)
    # X = MinMaxScaler().fit_transform(X)
    # X = pd.DataFrame(X, columns=xcols)
    # ##########################

    data = df_[xcols + ycols].rename(columns={ycols[0]: 'target'})
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, random_state=None)
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

# @SimpleNode # can not pickle
def train_gpr_tpot(l=None):
    # with auto tuning
    if l is None:
        l = get_data()
    config_dict = {
            'sklearn.gaussian_process.GaussianProcessRegressor': {
                'alpha':np.logspace(-10, 1, 12),
                },
            'sklearn.pipeline.FeatureUnion': {},
            'sklearn.preprocessing.QuantileTransformer': {},
            'sklearn.preprocessing.MinMaxScaler': {},
            # 'competitions.MyGP': {
            #     'alpha':np.logspace(-10, 1, 12),
            #     'mu_x': np.logspace(-1, 2, 4),
            #     'mu_y': np.logspace(-1, 2, 4),
            #     }
            }
    model = TPOTRegressor(config_dict=config_dict, crossover_rate=0.1, cv=5,
        disable_update_check=False, early_stop=None, generations=10,
        max_eval_time_mins=5, max_time_mins=None,
        # memory=os.path.join(_mydir, 'tpot_cache'),
        mutation_rate=0.9, n_jobs=-1, offspring_size=None,
        # periodic_checkpoint_folder='periodic_checkpoint_gpr_tpot',
        population_size=100,
        random_state=None, scoring=None, subsample=1.0, use_dask=False,
        verbosity=3, warm_start=False)
    model.fit(l.X_train.copy(), l.y_train.copy().squeeze())
    model.export('tpot_gpr.py')
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

_tpot_cache = os.path.join(_mydir, 'tpot_cache')
if not os.path.exists(_tpot_cache):
    os.makedirs(_tpot_cache)

@SimpleNode
def train_tpot(l=None):
    # can also do directly from the command line
    if l is None:
        l = get_data()
    model = TPOTRegressor(config_dict=None, crossover_rate=0.1, cv=5,
        disable_update_check=False, early_stop=None, generations=100,
        max_eval_time_mins=5, max_time_mins=None, memory=_tpot_cache,
        mutation_rate=0.9, n_jobs=-1, offspring_size=None,
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
    # df = d.df; df = df[df.r > 0]
    r = linspace(d.X_train.r.min(), d.X_train.r.max(), mm)
    days_remaining = linspace(d.X_train.days_remaining.min(), d.X_train.days_remaining.max(), n)
    X, Y = meshgrid(r, days_remaining)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    Z = model.predict(xy).reshape(X.shape)

    fig = plt.figure(2)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, linewidth=1, alpha=0.5)
    ax.scatter(d.X_train.r, d.X_train.days_remaining, d.y_train.values, 'bo', alpha=0.5, label='train')
    ax.scatter(d.X_test.r, d.X_test.days_remaining, d.y_test.values, 'ro', alpha=0.5, label='train')
    ax.set_xlabel('r')
    # ax.set_xscale('log')
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
    # df_orig = l['df']
    # df = df_orig[df_orig.r > 0]
    # do_plots(df=df)
    # l = train_svm()
    # plot_predict(l.model)
