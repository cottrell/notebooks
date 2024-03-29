"""
Some example to show tricks for trying to work with inputs that do not have a common "batch_size".

Network is a separable representation h(f(S) * g(X)) where f outputs a scalar and g and h operate element wise across the vectors.
"""
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np

m = 100
n = 3
d = 12
S = np.random.randn(m, n)
X = np.arange(d)

S_in = keras.layers.Input(shape=(n,), name='S_in')
X_in = keras.layers.Input(shape=(d,), name='X_in')
s = S_in
for k in [16, 16, 1]:
    s = keras.layers.Dense(k, activation='tanh')(s)
x = tf.expand_dims(X_in, axis=2)
for k in [8, 8, 1]:
    x = keras.layers.Conv1D(k, 1, activation='tanh')(x)
assert s.shape.as_list() == [None, 1]
assert x.shape.as_list() == [None, d, 1]
s = tf.expand_dims(s, axis=1)
l = tf.multiply(s, x) # broadcasting
assert l.shape.as_list() == [None, d, 1]
for k in [8, 8, 1]:
    l = keras.layers.Conv1D(k, 1, activation='tanh')(l)
l = tf.squeeze(l, axis=-1)
assert l.shape.as_list() == [None, d]
model = keras.models.Model(inputs=[S_in, X_in], outputs=l)
model.compile(loss=keras.losses.MeanSquaredError(), optimizer=keras.optimizers.Adam())

# this fails
try:
    pred1 = model.predict([S, X])
    print('should not hit this')
except Exception as e:
    print(e)

# this works
XX = np.repeat(np.atleast_2d(X), m, axis=0)
pred = model.predict([S, XX])
plt.ion()
fig = plt.figure(1)
fig.clf()
plt.plot(pred.T)
plt.show()
