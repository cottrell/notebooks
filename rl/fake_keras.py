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

def glorot_uniform_replace(shape):
    fan_in, fan_out = shape
    limit = np.sqrt(6 / (fan_in + fan_out))
    return (np.random.rand(*shape) * 2 - 1) * limit


def fixed_size_random_keras_network(input_dim, output_dim, initial_layers=None,
        dims=[4, 4, 4, 4],
        final_activation='linear',
        bias_dist=scipy.stats.norm(loc=0, scale=0).rvs, # turn it off
        weight_dist=glorot_uniform_replace, # scipy.stats.norm().rvs,
        use_bias=True,
        batch_normalize=False,
        **kwargs):
    """
    TODO: use glorot_uniform random: It draws samples from a uniform distribution within [-limit, limit] where limit is sqrt(6 / (fan_in + fan_out)) where fan_in is the number of input units in the weight tensor and fan_out is the number of output units in the weight tensor.
    TODO: keras weights are per layer. Each layer looks like it has two weights: the weights matrix and the bias. You probably want to treat each separately or apply a batch norm or something.
    """
    dims = [input_dim] + dims + [output_dim]
    import tensorflow.keras as k
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import BatchNormalization
    # BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros',
    # moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)

    from tensorflow.keras.layers import Dense
    if initial_layers is not None:
        layers = list(initial_layers)
    else:
        layers = list()
    kernel_initializer = kwargs.get('kernel_initializer', 'glorot_uniform')
    random_weights = dict()
    for i in range(len(dims) - 1):
        activation = 'relu' if i < (len(dims) - 1) else final_activation
        # not sure if supplying input dims in middle layers is bad
        layers.append(Dense(dims[i+1], input_dim=dims[i], kernel_initializer=kernel_initializer, activation=activation, use_bias=use_bias))
        random_weights[len(layers) - 1] = True
        if batch_normalize:
            layers.append(BatchNormalization())
    layers.append(Dense(dims[-1], kernel_initializer=kernel_initializer, activation=final_activation))
    random_weights[len(layers) - 1] = True
    model = Sequential(layers)
    # call predict to initialize the weights? not sure how else to do this
    _ = model.predict(np.random.randn(1, input_dim))
    for k in random_weights:
        # print(len(model.layers[k].get_weights()))
        w = model.layers[k].get_weights()
        w[0] = weight_dist(w[0].shape)
        if model.layers[k].use_bias:
            assert len(w) == 2
            w[1] = bias_dist(w[1].shape)
        else:
            assert len(w) == 1
        model.layers[k].set_weights(w)
    return model

# probably could use tpot or autokeras utils to do this
def random_keras_network(input_dim, output_dim,
        min_layer_dim=3,
        layer_dim_dist=scipy.stats.poisson(4), # dimension of layers
        min_layers=3,
        n_layers_dist=scipy.stats.poisson(3), # number of layers
        final_activiation='linear',
        weight_dist=scipy.stats.norm(),
        **kwargs):
    n_layers = max(min_layers, n_layers_dist.rvs())
    dims = [input_dim] + layer_dim_dist.rvs(n_layers).tolist() + [output_dim]
    import tensorflow.keras as k
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense
    layers = list()
    kernel_initializer = kwargs.get('kernel_initializer', 'glorot_uniform')
    for i in range(len(dims) - 1):
        activation = 'relu' if i < (len(dims) - 1) else final_activiation
        # not sure if supplying input dims in middle layers is bad
        layers.append(Dense(dims[i+1], input_dim=dims[i], kernel_initializer=kernel_initializer, activation=activation))
    layers.append(Dense(dims[-1], kernel_initializer=kernel_initializer, activation=final_activiation))
    model = Sequential(layers)
    # call predict to initialize the weights, not sure how else to do this
    _ = model.predict(np.random.randn(1, input_dim))
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
    a = np.random.randn(1, input_dim).astype(np.float32)
    g = GradientHelper(model)
    print(g(a))

def default_summary():
    # tf.reset_default_graph()
    writer = tf.summary.FileWriter('.')
    writer.add_graph(tf.get_default_graph())
