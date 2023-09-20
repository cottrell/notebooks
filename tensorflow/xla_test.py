#!/usr/bin/env python
import os
import tensorflow as tf

# LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/TensorRT-8.6.1.6/lib'

@tf.function(experimental_compile=True)
def xla_test_function(x):
    return x * x

def main():
    os.environ['TF_XLA_FLAGS'] = '--tf_xla_auto_jit=2'
    x = tf.constant([1.0, 2.0, 3.0])
    print(xla_test_function(x))

if __name__ == '__main__':
    main()
