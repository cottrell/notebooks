# pip install tf-nightly-gpu
import tensorflow as tf
import tensorflow.keras.activations as ka
import tensorflow.keras.backend as K
import tensorflow.keras.layers as kl
import tensorflow.keras.models as km
import numpy as np

class Model(km.Model):
    def __init__(self, dim):
        X_input = kl.Input(shape=(None, dim))
        Z_input = kl.Input(shape=(None, None, 1))
        super().__init__()
        self.dim = dim
    def call(self, inputs):
        X, Z = inputs
        X_layer = kl.Dense(16, activation='linear')(X)
        Z_dense = kl.Dense(16, activation='linear')
        combined = list()
        for i in range(Z.shape[1]):
            z = Z_dense(Z[:,i])
            l = X_layer + z
            l = K.expand_dims(l, axis=1)
            combined.append(l)
        combined = kl.concatenate(combined, axis=1)
        # combined is now shape (batch_size, z_size, 16)
        l = ka.relu(combined)
        l = kl.Dense(16, activation='relu')(l)
        l = kl.Dense(16, activation='relu')(l)
        l = kl.Dense(16, activation='linear')(l)
        return l

dim = 6
m = 100
X = np.random.randn(m, dim)
Z = np.random.randn(m, 10, 1)

model = Model(dim)

out = model.predict([X, Z])
