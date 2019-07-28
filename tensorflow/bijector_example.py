import tensorflow as tf
import tensorflow_probability as tfp
tfb = tfp.bijectors
tfd = tfp.distributions


class BijectorBase(tfb.Bijector):

    def transformed_log_prob(self, log_prob, x):
        return (self.inverse_log_det_jacobian(x, event_ndims=0) + log_prob(tfp.bijector.inverse(x)))

    def transformed_sample(self, x):
        return tfp.bijector.forward(x)


# quite easy to interpret - multiplying by alpha causes a contraction in volume.
class LeakyReLU(BijectorBase):

    def __init__(self, alpha=0.5, validate_args=False, name="leaky_relu"):
        super().__init__(event_ndims=1, validate_args=validate_args, name=name)
        self.alpha = alpha

    def _forward(self, x):
        return tf.where(tf.greater_equal(x, 0), x, self.alpha * x)

    def _inverse(self, y):
        return tf.where(tf.greater_equal(y, 0), y, 1. / self.alpha * y)

    def _inverse_log_det_jacobian(self, y):
        event_dims = self._event_dims_tensor(y)
        I = tf.ones_like(y)
        J_inv = tf.where(tf.greater_equal(y, 0), I, 1.0 / self.alpha * I)
        # abs is actually redundant here, since this det Jacobian is > 0
        log_abs_det_J_inv = tf.math.log(tf.abs(J_inv))
        return tf.reduce_sum(log_abs_det_J_inv, axis=event_dims)

class Exp(BijectorBase):

    def __init__(self, validate_args=False, name="exp"):
        super(Exp, self).__init__(
            validate_args=validate_args,
            forward_min_event_ndims=0,
            name=name)

    def _forward(self, x):
        return tf.math.exp(x)

    def _inverse(self, y):
        return tf.math.log(y)

    def _inverse_log_det_jacobian(self, y):
        return -self._forward_log_det_jacobian(self._inverse(y))
        # return -self._forward_log_det_jac(self._inverse(y))  # Note negation. alt version

    def _forward_log_det_jacobian(self, x):
        # Notice that we needn't do any reducing, even when`event_ndims > 0`.
        # The base Bijector class will handle reducing for us; it knows how
        # to do so because we called `super` `__init__` with
        # `forward_min_event_ndims = 0`.
        return x


class TrainStepper():
    def __init__(self, optimizer, model):
        self.optimizer = optimizer
        self.model = model
        self._debug = False
        self._tfcall = tf.function(self._call)
        self.step = 0

    def debug(self, value=None):
        if value is None:
            self._debug = not self._debug
        else:
            self._debug = value
        print(f'debug={self.debug}')

    def __call__(self, *data):
        self.step += 1
        if self._debug:
            return self._call(*data)
        else:
            return self._tfcall(*data)

    def _call(self, *data):
        with tf.GradientTape() as tape:
            d = self.model(*data)
        print(self.model.trainable_variables)
        gradients = tape.gradient(d['loss'], self.model.trainable_variables)
        _ = self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return d

    def train(self, data, epochs=1000, log_period=100):
        for epoch in range(epochs):
            d = self(*data)
            if self.step % log_period == 0:
                print({k: v.numpy() for k, v in d.items()})
                for k, v in d.items():
                    tf.summary.scalar(k, v, step=self.step)

import numpy as np
x = np.random.rand(100, 1) * 2.34 + 7.3

class MyLayer(tf.keras.models.Model):

    def __init__(self):
        super().__init__()
        self.bijectors = list()
        self.shift = tf.Variable([0.], dtype=tf.float32, name='shift')
        self.scale_diag = tf.Variable([10.], dtype=tf.float32, name='scale_diag')
        self.bijectors.append(tfb.Affine(shift=self.shift, scale_diag=self.scale_diag))
        self.bijectors.append(Exp())
        self.bijector = tfb.Chain(self.bijectors[::-1])
        self.model = tfd.TransformedDistribution(
                        distribution=tfd.Uniform(),
                        bijector=self.bijector,
                        event_shape=(1,))

    def call(self, *inputs):
        return self.model(*inputs)

class LossModel(tf.keras.models.Model):

    def __init__(self, bijector_layer):
        super().__init__()
        self.model = bijector_layer

    def call(self, *x):
        return dict(loss=tf.reduce_mean(self.model.model.log_prob(x)))

mylayer = MyLayer()
lossmodel = LossModel(mylayer)
optimizer = tf.optimizers.Adam(learning_rate=0.001)
stepper = TrainStepper(optimizer=optimizer, model=lossmodel)


with tf.GradientTape() as tape:
    loss = mylayer.model.log_prob(x)
gradients = tape.gradient(loss, mylayer.trainable_variables)
# _ = optimizer.apply_gradients(zip(gradients, mylayer.trainable_variables))
