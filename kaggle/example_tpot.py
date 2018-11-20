from tpot import TPOTRegressor
import sklearn.base
from sklearn.gaussian_process import GaussianProcessRegressor, kernels
import numpy as np

X = np.random.randn(100, 2)
y = np.random.randn(100)

class MyGP(GaussianProcessRegressor, sklearn.base.RegressorMixin):
    def __init__(self, alpha=1, mu_x=1, mu_y=1):
        mu = np.array([mu_x, mu_y])
        super().__init__(alpha=alpha, copy_X_train=True, kernel=kernels.RBF(mu),
            n_restarts_optimizer=0, normalize_y=False,
            optimizer='fmin_l_bfgs_b', random_state=None)

def works():
    config_dict = {
        'sklearn.gaussian_process.GaussianProcessRegressor': {
            'alpha': [1e1, 1, 1e-1]
            }
        }
    model = TPOTRegressor(config_dict=config_dict, crossover_rate=0.1, cv=5,
        disable_update_check=False, early_stop=None, generations=10,
        max_eval_time_mins=5, max_time_mins=None,
        mutation_rate=0.9, n_jobs=-1, offspring_size=None,
        population_size=100,
        random_state=None, scoring=None, subsample=1.0, use_dask=False,
        verbosity=3, warm_start=False)
    model.fit(X, y)

def fails():
    config_dict = {
        'example_tpot.MyGP': {
            'alpha': [1e1, 1, 1e-1],
            # 'mu_x': np.logspace(-2, 4, 10),
            # 'mu_y': np.logspace(-2, 4, 10),
            }
        }
    model = TPOTRegressor(config_dict=config_dict, crossover_rate=0.1, cv=5,
        disable_update_check=False, early_stop=None, generations=10,
        max_eval_time_mins=5, max_time_mins=None,
        mutation_rate=0.9, n_jobs=-1, offspring_size=None,
        population_size=100,
        random_state=None, scoring=None, subsample=1.0, use_dask=False,
        verbosity=3, warm_start=False)
    model.fit(X, y)
