from pylab import *
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_probability as tfp
tfb = tfp.bijectors
tfd = tfp.distributions

# class NVPLayer(tf.keras.layers.Layer):
class NVPLayer(tf.keras.models.Model):

    def __init__(self, *, output_dim, num_masked, **kwargs):
        super().__init__(**kwargs)
        self.output_dim = output_dim
        self.num_masked = num_masked
        self.shift_and_log_scale_fn = tfb.real_nvp_default_template(
            hidden_layers=[2],
            activation=None, # linear
            )
        self.loss = None

    def call(self, *inputs):
        nvp = tfd.TransformedDistribution(
            distribution=tfd.MultivariateNormalDiag(loc=[0., 0., 0.]),
            bijector=tfb.RealNVP(
                num_masked=self.num_masked,
                shift_and_log_scale_fn=self.shift_and_log_scale_fn)
            )
        self.loss = tf.reduce_mean(nvp.log_prob(*inputs)) # how else to do this?
        return nvp.bijector.forward(*inputs)

layer = NVPLayer(output_dim=3, num_masked=1)
x = (np.random.randn(100, 3) * np.array([1, 3, 5]) + np.array([-3, -10, 4])).astype(np.float32)
z0 = layer(x).numpy()

optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
for i in range(1000):
    with tf.GradientTape() as tape:
        y = layer(x)
        loss = - layer.loss
        print(loss)
    g = tape.gradient(loss, layer.trainable_variables)
    l = optimizer.apply_gradients(zip(g, layer.trainable_variables))

z1 = layer(x).numpy()

print(pd.DataFrame(z0).describe())
print(pd.DataFrame(z1).describe())
