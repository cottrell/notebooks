import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K

m = 10000
mu = 0.1
sigma = 0.2
z = np.random.randn(m)
x = np.exp(mu + sigma * z)

class MyLayer(keras.layers.Layer):
    def __init__(self, output_dim=1, **kwargs):
        self.output_dim = output_dim
        super(MyLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.mu = self.add_weight(name='mu', shape=(1,), initializer='zeros', trainable=True)
        self.sigma = self.add_weight(name='sigma', shape=(1,), initializer='ones', trainable=True, constraint=keras.constraints.non_neg())
        super(MyLayer, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        log_probs = - tf.math.square(tf.math.log(x) - self.mu) / tf.math.square(self.sigma) / 2 - tf.math.log(x * self.sigma * np.sqrt(2 * np.pi))
        tf.debugging.assert_all_finite(log_probs, 'log_probs are nan')
        loss = -tf.reduce_mean(log_probs)
        self.add_loss(loss)
        return x

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)

x_in = keras.layers.Input(shape=(1,))
layer = MyLayer(name='dist')
log_probs = layer(x_in)
model = keras.models.Model(inputs=x_in, outputs=log_probs)
model.compile(loss=None, optimizer=keras.optimizers.Adam(learning_rate=0.001))
l_ = model.fit(x, verbose=1, batch_size=None, epochs=100)
l = model.get_layer('dist')
print(f'mu={l.mu.numpy()[0]}, sigma={l.sigma.numpy()[0]}')





# # mu_ = tf.Variable(1, name='mu', trainable=True, dtype=tf.float32)
# # sigma_ = tf.Variable(1, name='sigma', trainable=True, dtype=tf.float32)
# class MyLayer(keras.layers.Layer):
#     def __init__(self, **kwargs):
#         super(MyLayer, self).__init__(**kwargs)
# 
#     def build(self, input_shape):
#         self.kernel = self.add_weight(name='kernel', shape=(2,), initializer='ones', trainable=True)
#         super(MyLayer, self).build(2)
# 
#     def call(self, x):
#         # mu = self.kernel[0]
#         # sigma = self.kernel[1]
#         # return tf.math.square(x)
#         # return tf.math.square(tf.math.log(x))
#         return tf.math.square(tf.math.log(x) - mu) / 2 / tf.math.square(sigma) - tf.math.log(x * sigma * np.sqrt(2 * np.pi))
# 
#     def compute_output_shape(self, input_shape):
#         return (input_shape,)
# 
# # do something hacky to make keras work
# def custom_loss(layer):
#     def loss(log_probs, junk):
#         return -tf.reduce_sum(log_probs)
#     return loss
# 
x_in = keras.layers.Input(shape=(1,))
layer = MyLayer()
log_probs = layer(x_in)
# model2 = keras.models.Model(inputs=x_in, outputs=log_probs)
# model2.compile(loss=custom_loss(log_probs), optimizer=keras.optimizers.Adam(learning_rate=0.1))
# # z = np.zeros(m)
# # l = model.fit(x, z, verbose=1, batch_size=2048, epochs=100)
# 
# # putting @tf.function here causes errors
# def log_prob(x):
#     return tf.math.square(tf.math.log(x) - mu_) / 2 / tf.math.square(sigma_) - tf.math.log(x * sigma_ * np.sqrt(2 * np.pi))

# x_in = keras.layers.Input(shape=(1,))
# log_probs = log_prob(x_in)
# y = -tf.squeeze(tf.reduce_sum(log_probs, axis=0))
# z = np.zeros((1, 1))

# this approach does not work
# model = keras.models.Model(inputs=x_in, outputs=y)
# model.compile(loss=keras.losses.MeanAbsoluteError(), optimizer=keras.optimizers.Adam(learning_rate=0.1))
# model.fit(x, z, verbose=1, batch_size=128, steps_per_epoch=100)

# 
# model2 = keras.models.Model(inputs=x_in, outputs=log_probs)
# model2.compile(loss=custom_loss(log_probs), optimizer=keras.optimizers.Adam(learning_rate=0.1))
# z = np.zeros(m)
# l = model.fit(x, z, verbose=1, batch_size=2048, epochs=100)
