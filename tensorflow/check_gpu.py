#!/usr/bin/env python
import tensorflow as tf

devices = tf.config.list_physical_devices('GPU')

if devices:
    print('found GPU devices:')
    print(devices)
else:
    print("TF cannot find GPU")
