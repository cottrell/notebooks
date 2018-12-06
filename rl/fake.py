"""
Interested here in:

    * generating random networks
    * distribution of sensitivities
    * understanding ways of interpolating between two networks and what the responses look like on the paths between them
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
def gradients(model):
    gradients = tf.gradients(model.outputs, model.inputs)
    return gradients

def test():
    input_dim = 3
    output_dim = 1
    model = random_keras_network(input_dim, output_dim)
    g = gradients(model)
    x = g[0]
    with tf.Session() as sess:
        print(sess.run(x))


def default_summary():
    writer = tf.summary.FileWriter('.')
    writer.add_graph(tf.get_default_graph())

