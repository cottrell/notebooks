""" this one is failing. see dist_working """
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K
import pandas as pd
from pylab import *
ion()

m = 10000
mu = 0.1
sigma = 0.2
z = np.random.randn(m)
x = mu + sigma * z

import my.extractors as e
df = e.e.pdr_yahoo_price_volume.load(filters=[('symbol', '=', 'ibm')])
r = df.close.pct_change().dropna()
r = np.log(df.close).diff().dropna()

class LogNormalLayer(keras.layers.Layer):
    def __init__(self, output_dim=1, **kwargs):
        self.output_dim = output_dim
        super().__init__(**kwargs)

    def build(self, input_shape):
        self.mu = self.add_weight(name='mu', shape=(1,), initializer='zeros', trainable=True)
        self.sigma = self.add_weight(name='sigma', shape=(1,), initializer='ones', trainable=True, constraint=keras.constraints.non_neg())
        self.params = dict(mu=mu, sigma=sigma)
        super().build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        log_probs = - tf.math.square(tf.math.log(x) - self.mu) / tf.math.square(self.sigma) / 2 - tf.math.log(x * self.sigma * np.sqrt(2 * np.pi))
        tf.debugging.assert_all_finite(log_probs, 'log_probs are nan')
        loss = -tf.reduce_mean(log_probs)
        self.add_loss(loss)
        return x

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)

    def get_params(self):
        return {k: v.numpy() for k, v in self.params.items()}

def pareto_log_pdf(x, x_m, alpha):
    return tf.math.log(alpha) + alpha * tf.math.log(x_m) - (1 + alpha) * tf.math.log(x)

def norm_log_pdf(x, mu, sigma):
    return - tf.math.square(x - mu) / 2 / sigma ** 2 - tf.math.log(np.sqrt(2 * np.pi) * sigma)

class ParetoTail(keras.layers.Layer):
    def __init__(self, output_dim=1, **kwargs):
        self.output_dim = output_dim
        super(ParetoTail, self).__init__(**kwargs)

    def build(self, input_shape):
        params = dict()
        mu = K.variable(0)
        sigma = K.variable(0.1, constraint=keras.constraints.non_neg()) # , constraint=lambda x: max(0, x))
        x_up = K.variable(0.1, constraint=keras.constraints.non_neg()) # , constraint=lambda x: max(0, x))
        x_down = K.variable(0.1, constraint=keras.constraints.non_neg()) # , constraint=lambda x: max(0, x))
        alpha_up = K.variable(0.5, constraint=keras.constraints.non_neg()) # , constraint=lambda x: max(0, x))
        alpha_down = K.variable(0.5, constraint=keras.constraints.non_neg()) # , constraint=lambda x: max(0, x))
        self.params = dict(mu=mu, sigma=sigma, x_up=x_up, x_down=x_down, alpha_up=alpha_up, alpha_down=alpha_down)
        super().build(input_shape)

    def call(self, x):
        # log_probs_up = pareto_log_pdf(x, self.params['x_up'], self.params['alpha_up'])
        # tf.debugging.assert_all_finite(log_probs_up, 'log_probs are nan')
        # log_probs_down = pareto_log_pdf(-x, self.params['x_down'], self.params['alpha_down'])
        # tf.debugging.assert_all_finite(log_probs_down, 'log_probs are nan')
        # log_probs_center = norm_log_pdf(x, self.params['mu'], self.params['sigma'])
        # tf.debugging.assert_all_finite(log_probs_center, 'log_probs are nan')
        # log_probs = tf.where(x < -self.params['x_down'],
        #         log_probs_down, tf.where(x > self.params['x_up'],
        #             log_probs_up, log_probs_center))
        # tf.debugging.assert_all_finite(log_probs, 'log_probs are nan')
        log_probs = tf.math.square(x - self.params['mu']) # log_probs_center # DEBUG
        loss = -tf.reduce_mean(log_probs)
        self.add_loss(loss)
        return log_probs

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)

    def get_params(self):
        return {k: v.numpy() for k, v in self.params.items()}

class Estimator(keras.models.Model):
    def __init__(self, layer=ParetoTail, learning_rate=0.000000001):
        super().__init__()
        x_in = keras.layers.Input(shape=(1,))
        self.layer = ParetoTail(name='dist')
        self.log_probs = self.layer(x_in)
        self.model = keras.models.Model(inputs=x_in, outputs=self.log_probs)
        self.model.compile(loss=None, optimizer=keras.optimizers.Adam(learning_rate=learning_rate))

    def fit(self, x, batch_size=None, epochs=1, **kwargs):
        # self.layer.params['mu'].assign(np.mean(x))
        # self.layer.params['sigma'].assign(np.std(x))
        l = self.model.fit(x, verbose=1, batch_size=batch_size, epochs=epochs)

    def get_params(self):
        return self.model.get_layer('dist').get_params()

m = 10000
mu = 0.1
sigma = 0.2
z = np.random.randn(m)
x = np.exp(mu + sigma * z)

import scipy.stats as ss

# # a = r.values.copy()
# a = x
# a.sort()
# n = a.shape[0]
# p = np.linspace(1/n, 1 - 1/n, n)

# ss_norm = ss.norm(*ss.norm.fit(a ** 2))
estimator = Estimator(layer=LogNormalLayer)
# s = pd.Series(estimator.model.predict([-1, 0, 1]).squeeze())
# print(estimator.get_params())
estimator.fit(x)
# print(estimator.get_params())

# figure(1)
# fig = subplot(3, 1, 1)
# clf()
# hist(a, bins=200, alpha=0.3, density=True)
# grid()
# ax = twinx()
# ax.semilogy(a, p, 'b.-', alpha=0.5)
# ax.semilogy(a, 1-p, 'b.-', alpha=0.5)
# ax.semilogy(ss_norm.ppf(p), p, 'r-', alpha=0.2)
# ax.semilogy(ss_norm.ppf(p), 1-p, 'r-', alpha=0.2)
# show()
