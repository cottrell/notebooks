import tensorflow as tf
# tf.enable_eager_execution()
import tensorflow_probability as tfp
import numpy as np
import seaborn as sns
from pylab import *
import functools
import matplotlib.pyplot as plt
plt.style.use('ggplot')
sns.set_context('notebook')
tfb = tfp.bijectors
tfd = tfp.distributions

import extractors as e
df = e.e.pdr_yahoo_fx.load()


