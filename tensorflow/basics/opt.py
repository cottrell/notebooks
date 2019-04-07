# https://stackoverflow.com/questions/55552715/tensorflow-2-0-no-gradients-provided-for-any-variable/55558491#55558491
import numpy as np
import tensorflow as tf

x = tf.Variable(3, name='x', trainable=True, dtype=tf.float32)
with tf.GradientTape(persistent=True) as t:
    # log_x = tf.math.log(x)
    # y = tf.math.square(log_x)
    y = (x - 1) ** 2

opt = tf.optimizers.Adam(learning_rate=0.001)

def get_gradient_wrong(x0):
    # this does not work, it does not actually update the value of x
    x.assign(x0)
    return t.gradient(y, [x])

def get_gradient(x0):
    # this works
    x.assign(x0)
    with tf.GradientTape(persistent=True) as t:
        y = (x - 1) ** 2
    return t.gradient(y, [x])

#### Option 1
def a(x0, tol=1e-8, max_iter=10000):
    # does not appear to work properly
    x.assign(x0)
    err = np.Inf # step error (banach), not actual erro
    i = 0
    while err > tol:
        x0 = x.numpy()
        # IMPORTANT: WITHOUT THIS INSIDE THE LOOP THE GRADIENTS DO NOT UPDATE
        with tf.GradientTape(persistent=True) as t:
            y = (x - 1) ** 2
        gradients = t.gradient(y, [x])
        l = opt.apply_gradients(zip(gradients, [x]))
        err = np.abs(x.numpy() - x0)
        print(err, x.numpy(), gradients[0].numpy())
        i += 1
        if i > max_iter:
            print(f'stopping at max_iter={max_iter}')
            return x.numpy()
    print(f'stopping at err={err}<{tol}')
    return x.numpy()

#### Option 2
def b(x0, tol=1e-8, max_iter=10000):
    x.assign(x0)
    # To use minimize you have to define your loss computation as a funcction
    def compute_loss():
        log_x = tf.math.log(x)
        y = tf.math.square(log_x)
        return y
    err = np.Inf # step error (banach), not actual erro
    i = 0
    while err > tol:
        x0 = x.numpy()
        train = opt.minimize(compute_loss, var_list=[x])
        err = np.abs(x.numpy() - x0)
        print(err, x.numpy())
        i += 1
        if i > max_iter:
            print(f'stopping at max_iter={max_iter}')
            return x.numpy()
    print(f'stopping at err={err}<{tol}')
    return x.numpy()


# NOPE
# import tensorflow as tf
# x = tf.Variable(3.0)
# y = (x - 10) ** 2
# opt = tf.optimizers.Adam()
# opt.minimize(y, var_list=[x])
