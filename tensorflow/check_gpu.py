#!/usr/bin/env python
import tensorflow as tf

print(tf.config.list_physical_devices('GPU'))

if tf.test.is_gpu_available():
    print(tf.test.gpu_device_name())
else:
    print("TF cannot find GPU")
