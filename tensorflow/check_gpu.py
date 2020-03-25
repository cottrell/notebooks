#!/usr/bin/env python
import tensorflow as tf
# print("cuda_only=False", tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))
# print("")
# print("cuda_only=True", tf.test.is_gpu_available(cuda_only=True, min_cuda_compute_capability=None))

print(tf.config.list_physical_devices('GPU'))
