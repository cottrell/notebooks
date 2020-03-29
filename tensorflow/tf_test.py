"""
build just does not really work with the subclass api
"""
import numpy as np
import tensorflow as tf

class Test(tf.keras.models.Model):

    def __init__(self):
        super().__init__()
        self.dense = tf.keras.layers.Dense(units=1)

    def call(self, x):
        return self.dense(x)

    def build(self, input_shape):
        # self._set_inputs(input_shape) # ValueError: Model inputs are already set.
        # super().build(input_shape) # AttributeError: The layer has never been called and thus has no defined input shape.
        self.built = True

model = Test()
x = np.random.randn(100, 4)
model(x)
print(model.input_shape)
# model.save('here.tf')
