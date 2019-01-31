# https://github.com/tensorflow/probability/blob/master/tensorflow_probability/examples/jupyter_notebooks/Bayesian_Gaussian_Mixture_Model.ipynb
# see installers/tf.sh and source activate tf
# Create a mixture of two Gaussians:
import tensorflow_probability as tfp
import numpy as np
import tensorflow as tf
import seaborn as sns
# tf.enable_eager_execution()
from pylab import *
import functools
import matplotlib.pyplot as plt
plt.style.use('ggplot')
sns.set_context('notebook')
tfb = tfp.bijectors
tfd = tfp.distributions
# tf.enable_eager_execution()
tfd = tfp.distributions

import extractors as e
df = e.e.pdr_yahoo_fx.load()


def testplot():
    mix = 0.3
    bimix_gauss = tfd.Mixture(
        cat=tfd.Categorical(probs=[mix, 1.-mix]),
        components=[
            tfd.Normal(loc=-1., scale=0.1),
            tfd.Normal(loc=+1., scale=0.5),
        ])

    # Plot the PDF.
    sess = tf.InteractiveSession()
    ion()
    figure()
    with sess.as_default():
        x = tf.linspace(-2., 3., int(1e4)).eval()
        plt.plot(x, bimix_gauss.prob(x).eval())
        show()


def testplot2():
    num_vars = 2        # Number of variables (`n` in formula).
    var_dim = 1         # Dimensionality of each variable `x[i]`.
    num_components = 3  # Number of components for each mixture (`K` in formula).
    sigma = 5e-2        # Fixed standard deviation of each component.

    # Set seed. Remove this line to generate different mixtures!
    tf.set_random_seed(77)

    # Choose some random (component) modes.
    component_mean = tfd.Uniform().sample([num_vars, num_components, var_dim])

    factorial_mog = tfd.Independent(
        tfd.MixtureSameFamily(
            # Assume uniform weight on each component.
            mixture_distribution=tfd.Categorical(
                logits=tf.zeros([num_vars, num_components])),
            components_distribution=tfd.MultivariateNormalDiag(
                loc=component_mean, scale_diag=[sigma])),
        reinterpreted_batch_ndims=1)
    plt.figure(figsize=(6, 5))

    # Compute density.
    nx = 250  # Number of bins per dimension.
    x = np.linspace(-3 * sigma, 1 + 3 * sigma, nx).astype('float32')
    vals = tf.reshape(tf.stack(np.meshgrid(x, x), axis=2), (-1, num_vars, var_dim))
    probs = factorial_mog.prob(vals).numpy().reshape(nx, nx)

    # Display as image.
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(sns.color_palette("Blues", 256))
    p = plt.pcolor(x, x, probs, cmap=cmap)
    ax = plt.axis('tight')

    # Plot locations of means.
    means_np = component_mean.numpy().squeeze()
    for mu_x in means_np[0]:
        for mu_y in means_np[1]:
            plt.scatter(mu_x, mu_y, s=150, marker='*', c='r', edgecolor='none')
    plt.axis(ax)

    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.title('Density of factorial mixture of Gaussians')
    plt.show()


def session_options(enable_gpu_ram_resizing=True):
    """Convenience function which sets common `tf.Session` options."""
    config = tf.ConfigProto()
    config.log_device_placement = True
    if enable_gpu_ram_resizing:
        # `allow_growth=True` makes it possible to connect multiple colabs to your
        # GPU. Otherwise the colab malloc's all GPU ram.
        config.gpu_options.allow_growth = True
    return config


def reset_sess(config=None):
    """Convenience function to create the TF graph and session, or reset them."""
    if config is None:
        config = session_options()
    tf.reset_default_graph()
    global sess
    try:
        sess.close()
    except:
        pass
    sess = tf.InteractiveSession(config=config)


reset_sess()
# testplot()


class MVNCholPrecisionTriL(tfd.TransformedDistribution):
    """MVN from loc and (Cholesky) precision matrix."""

    def __init__(self, loc, chol_precision_tril, name=None):
        super(MVNCholPrecisionTriL, self).__init__(
            distribution=tfd.Independent(tfd.Normal(tf.zeros_like(loc),
                                                    scale=tf.ones_like(loc)),
                                         reinterpreted_batch_ndims=1),
            bijector=tfb.Chain([
                tfb.Affine(shift=loc),
                tfb.Invert(tfb.Affine(scale_tril=chol_precision_tril,
                                      adjoint=True)),
            ]),
            name=name)


def compute_sample_stats(d, seed=42, n=int(1e6)):
    x = d.sample(n, seed=seed)
    sample_mean = tf.reduce_mean(x, axis=0, keepdims=True)
    s = x - sample_mean
    sample_cov = tf.matmul(s, s, adjoint_a=True) / tf.cast(n, s.dtype)
    sample_scale = tf.cholesky(sample_cov)
    sample_mean = sample_mean[0]
    return [
        sample_mean,
        sample_cov,
        sample_scale,
    ]


def test_sample():
    dtype = np.float32
    true_loc = np.array([1., -1.], dtype=dtype)
    true_chol_precision = np.array([[1., 0.],
                                    [2., 8.]],
                                   dtype=dtype)
    true_precision = np.matmul(true_chol_precision, true_chol_precision.T)
    true_cov = np.linalg.inv(true_precision)

    d = MVNCholPrecisionTriL(
        loc=true_loc,
        chol_precision_tril=true_chol_precision)

    [
        sample_mean_,
        sample_cov_,
        sample_scale_,
    ] = sess.run(compute_sample_stats(d))

    print('true mean:', true_loc)
    print('sample mean:', sample_mean_)
    print('true cov:\n', true_cov)
    print('sample cov:\n', sample_cov_)


dtype = np.float32
dims = 2
components = 3


rv_mix_probs = tfd.Dirichlet(
    concentration=np.ones(components, dtype) / 10.,
    name='rv_mix_probs')

rv_loc = tfd.Independent(
    tfd.Normal(
        loc=np.stack([
            -np.ones(dims, dtype),
            np.zeros(dims, dtype),
            np.ones(dims, dtype),
        ]),
        scale=tf.ones([components, dims], dtype)),
    reinterpreted_batch_ndims=1,
    name='rv_loc')

rv_precision = tfd.Wishart(
    df=5,
    scale_tril=np.stack([np.eye(dims, dtype=dtype)]*components),
    input_output_cholesky=True,
    name='rv_precision')

print(rv_mix_probs)
print(rv_loc)
print(rv_precision)


def joint_log_prob(observations, mix_probs, loc, chol_precision):
    """BGMM with priors: loc=Normal, precision=Inverse-Wishart, mix=Dirichlet.

    Args:
      observations: `[n, d]`-shaped `Tensor` representing Bayesian Gaussian
        Mixture model draws. Each sample is a length-`d` vector.
      mix_probs: `[K]`-shaped `Tensor` representing random draw from
        `SoftmaxInverse(Dirichlet)` prior.
      loc: `[K, d]`-shaped `Tensor` representing the location parameter of the
        `K` components.
      chol_precision: `[K, d, d]`-shaped `Tensor` representing `K` lower
        triangular `cholesky(Precision)` matrices, each being sampled from
        a Wishart distribution.

    Returns:
      log_prob: `Tensor` representing joint log-density over all inputs.
    """
    rv_observations = tfd.MixtureSameFamily(
        mixture_distribution=tfd.Categorical(probs=mix_probs),
        components_distribution=MVNCholPrecisionTriL(
            loc=loc,
            chol_precision_tril=chol_precision))
    log_prob_parts = [
        rv_observations.log_prob(observations),  # Sum over samples.
        rv_mix_probs.log_prob(mix_probs)[..., tf.newaxis],
        rv_loc.log_prob(loc),                   # Sum over components.
        rv_precision.log_prob(chol_precision),  # Sum over components.
    ]
    sum_log_prob = tf.reduce_sum(tf.concat(log_prob_parts, axis=-1), axis=-1)
    # Note: for easy debugging, uncomment the following:
    # sum_log_prob = tf.Print(sum_log_prob, log_prob_parts)
    return sum_log_prob

# gen training data
num_samples = 1000
true_loc = np.array([[-2, -2],
                     [0, 0],
                     [2, 2]], dtype)
random = np.random.RandomState(seed=42)

true_hidden_component = random.randint(0, components, num_samples)
observations = (true_loc[true_hidden_component] + random.randn(num_samples, dims).astype(dtype))

# bayesian inferance
unnormalized_posterior_log_prob = functools.partial(joint_log_prob, observations)

initial_state = [
    tf.fill([components],
            value=np.array(1. / components, dtype),
            name='mix_probs'),
    tf.constant(np.array([[-2, -2],
                          [0, 0],
                          [2, 2]], dtype),
                name='loc'),
    tf.eye(dims, batch_shape=[components], dtype=dtype, name='chol_precision'),
]


unconstraining_bijectors = [
    tfb.SoftmaxCentered(),
    tfb.Identity(),
    tfb.Chain([
        tfb.TransformDiagonal(tfb.Softplus()),
        tfb.FillTriangular(),
    ])]

[mix_probs, loc, chol_precision], kernel_results = tfp.mcmc.sample_chain(
    num_results=2000,
    num_burnin_steps=500,
    current_state=initial_state,
    kernel=tfp.mcmc.TransformedTransitionKernel(
        inner_kernel=tfp.mcmc.HamiltonianMonteCarlo(
            target_log_prob_fn=unnormalized_posterior_log_prob,
            step_size=0.065,
            num_leapfrog_steps=5),
        bijector=unconstraining_bijectors))

acceptance_rate = tf.reduce_mean(tf.to_float(kernel_results.inner_results.is_accepted))
mean_mix_probs = tf.reduce_mean(mix_probs, axis=0)
mean_loc = tf.reduce_mean(loc, axis=0)
mean_chol_precision = tf.reduce_mean(chol_precision, axis=0)

[ acceptance_rate_,
  mean_mix_probs_,
  mean_loc_,
  mean_chol_precision_,
  mix_probs_,
  loc_,
  chol_precision_,
] = sess.run([
    acceptance_rate,
    mean_mix_probs,
    mean_loc,
    mean_chol_precision,
    mix_probs,
    loc,
    chol_precision,
])

print('    acceptance_rate:', acceptance_rate_)
print('      avg mix probs:', mean_mix_probs_)
print('\n            avg loc:\n', mean_loc_)
print('\navg chol(precision):\n', mean_chol_precision_)

ax = sns.kdeplot(loc_[:,0,0], loc_[:,0,1], shade=True)
ax = sns.kdeplot(loc_[:,1,0], loc_[:,1,1], shade=True)
ax = sns.kdeplot(loc_[:,2,0], loc_[:,2,1], shade=True)
plt.title('KDE of loc draws');
