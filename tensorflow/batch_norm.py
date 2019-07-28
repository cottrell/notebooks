import tensorflow_probability as tfp
tfd = tfp.distributions
tfb = tfp.bijectors

dist = tfd.TransformedDistribution(
    distribution=tfd.Normal(loc=[0], scale=[1]),
    bijector=tfb.BatchNormalization())

y = tfd.MultivariateNormalDiag(loc=[1.], scale_diag=[2.]).sample(100)  # ~ N(1, 2)
x = dist.bijector.inverse(y)  # ~ N(0, 1)

# THIS IS BUSTED
# y = dist.sample()  # ~ N(1, 2)
