import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
tfb = tfp.bijectors


batch_size=512
x2_dist = tfd.Normal(loc=0., scale=4.)
x2_samples = x2_dist.sample(batch_size)
x1 = tfd.Normal(loc=.25 * tf.square(x2_samples),
                        scale=tf.ones(batch_size, dtype=tf.float32))
x1_samples = x1.sample()
x_samples = tf.stack([x1_samples, x2_samples], axis=1)

base_dist = tfd.MultivariateNormalDiag(loc=tf.zeros([2], tf.float32))

class LeakyReLU(tfb.Bijector):
    def __init__(self, alpha=0.5, validate_args=False, name="leaky_relu"):
        super(LeakyReLU, self).__init__(
            1, validate_args=validate_args, name=name)
        self.alpha = alpha

    def _forward(self, x):
        return tf.compat.v1.where(tf.greater_equal(x, 0), x, self.alpha * x)

    def _inverse(self, y):
        return tf.compat.v1.where(tf.greater_equal(y, 0), y, 1. / self.alpha * y)

    def _inverse_log_det_jacobian(self, y):
        event_dims = self._event_dims_tensor(y)
        I = tf.ones_like(y)
        J_inv = tf.compat.v1.where(tf.greater_equal(y, 0), I, 1.0 / self.alpha * I)
        # abs is actually redundant here, since this det Jacobian is > 0
        log_abs_det_J_inv = tf.math.log(tf.abs(J_inv))
        return tf.reduce_sum(input_tensor=log_abs_det_J_inv, axis=event_dims)

d, r = 2, 2
DTYPE = tf.float32
bijectors = []
num_layers = 6
for i in range(num_layers):
    with tf.compat.v1.variable_scope('bijector_%d' % i):
        V = tf.compat.v1.get_variable('V', [d, r], dtype=DTYPE)  # factor loading
        shift = tf.compat.v1.get_variable('shift', [d], dtype=DTYPE)  # affine shift
        L = tf.compat.v1.get_variable('L', [d * (d + 1) / 2],
                            dtype=DTYPE)  # lower triangular
        bijectors.append(tfb.Affine(
            scale_tril=tfd.fill_triangular(L),
            scale_perturb_factor=V,
            shift=shift,
        ))
        alpha = tf.abs(tf.compat.v1.get_variable('alpha', [], dtype=DTYPE)) + .01
        bijectors.append(LeakyReLU(alpha=alpha))
# Last layer is affine. Note that tfb.Chain takes a list of bijectors in the *reverse* order
# that they are applied.
mlp_bijector = tfb.Chain(
    list(reversed(bijectors[:-1])), name='2d_mlp_bijector')
dist = tfd.TransformedDistribution(
    distribution=base_dist,
    bijector=mlp_bijector
)

loss = -tf.reduce_mean(input_tensor=dist.log_prob(x_samples))
train_op = tf.compat.v1.train.AdamOptimizer(1e-3).minimize(loss)
sess = tf.compat.v1.InteractiveSession()
sess.run(tf.compat.v1.global_variables_initializer())
NUM_STEPS = int(1e5)
global_step = []
np_losses = []
for i in range(NUM_STEPS):
    _, np_loss = sess.run([train_op, loss])
    if i % 1000 == 0:
        global_step.append(i)
        np_losses.append(np_loss)
    if i % int(1e4) == 0:
        print(i, np_loss)
