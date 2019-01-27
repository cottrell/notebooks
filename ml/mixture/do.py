# see installers/tf.sh and source activate tf
# Create a mixture of two Gaussians:
import tensorflow as tf
import tensorflow_probability as tfp
import matplotlib.pyplot as plt
from pylab import *
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
        plt.plot(x, bimix_gauss.prob(x).eval());
        show()

