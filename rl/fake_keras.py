"""
Interested here in:

    * generating random networks
    * distribution of sensitivities
    * understanding ways of interpolating between two networks and what the responses look like on the paths between them



https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/ops/parallel_for/gradients.py#L28
"""
import numpy as np
import scipy.sparse
import scipy.stats

# watch out
np.random.seed(0)

# probably could use tpot or autokeras utils to do this
def random_keras_network(input_dim, output_dim,
        min_layer_dim=3,
        layer_dim_dist=scipy.stats.poisson(12),
        min_layers=3,
        n_layers_dist=scipy.stats.poisson(8),
        final_activiation='linear',
        weight_dist=scipy.stats.norm(),
        **kwargs):
    # n_layers = max(min_layers, n_layers_dist.rvs())
    n_layers = 2
    dims = [input_dim] + layer_dim_dist.rvs(n_layers).tolist() + [output_dim]
    import tensorflow.keras as k
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense
    layers = list()
    kernel_initializer = kwargs.get('kernel_initializer', 'glorot_uniform')
    for i in range(len(dims) - 1):
        activation = 'relu' if i < (len(dims) - 1) else final_activiation
        layers.append(Dense(dims[i+1], kernel_initializer=kernel_initializer, activation=activation))
    layers.append(Dense(dims[-1], kernel_initializer=kernel_initializer, activation=final_activiation))
    model = Sequential(layers)
    # call predict to initialize the weights, not sure how else to do this
    _ = model.predict(np.random.randn(input_dim, 1))
    weights = model.get_weights()
    random_weights = [weight_dist.rvs(w.shape) for w in weights]
    model.set_weights(random_weights)
    return model

import tensorflow as tf
try:
    sess
except NameError as e:
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

class GradientHelper():
    def __init__(self, model, session=None):
        self.sess = sess
        if session is not None:
            self.sess = session
        self._x = model.inputs
        self._y = model.outputs
        self.gradients = tf.gradients(self._y, self._x)
    def __call__(self, *inputs):
        assert len(inputs) == len(self._x)
        return self.sess.run(self.gradients, feed_dict={x: v for x, v in zip(self._x, inputs)})


def test_GradientHelper():
    input_dim = 3
    output_dim = 1
    model = random_keras_network(input_dim, output_dim)
    a = np.random.randn(2, 1).astype(np.float32)
    g = GradientHelper(model)
    print(g(a))

def default_summary():
    # tf.reset_default_graph()
    writer = tf.summary.FileWriter('.')
    writer.add_graph(tf.get_default_graph())
