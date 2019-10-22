import tensorflow as tf

class A(tf.keras.models.Model):
    def __init__(self):
        self.something = tf.keras.backend.variable(1, dtype=tf.float32, name='something')
        super().__init__()

a = A()
filename = '/tmp/test_weights'
print(a.trainable_weights)
print(a.something)
a.something.assign(1.2)
print('before save', a.something)
a.save_weights(filename)
print('after save', a.something)
a.load_weights(filename)
print('after load', a.something)
print(a.something)
