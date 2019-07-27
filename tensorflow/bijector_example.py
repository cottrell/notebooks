import tensorflow as tf
import tensorflow_probability as tfp


class BijectorBase(tfp.bijectors.Bijector):

    def transformed_log_prob(self, log_prob, x):
        return (self.inverse_log_det_jacobian(x, event_ndims=0) + log_prob(tfp.bijector.inverse(x)))

    def transformed_sample(self, x):
        return tfp.bijector.forward(x)


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
        gradients = tape.gradient(d['loss'], self.model.trainable_variables)
        l = self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return d

model = Exp()
import numpy as np
x = np.random.randn(100) * 2.34 + 7.3
print(model(x))


optimizer = tf.optimizers.Adam(learning_rate=0.001)
lossmodel = model
stepper = TrainStepper(optimizer=optimizer, model=lossmodel)
