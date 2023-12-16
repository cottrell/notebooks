#!/usr/bin/env python
import tensorflow as tf

devices = tf.config.list_physical_devices('GPU')

import os

# NOTE: 2023-12-16 you no longer needed.
#
# print(f'NOTE: LD_LIBRARY_PATH={os.environ["LD_LIBRARY_PATH"]} ... 2023-08-04 you needed this as in the comment in this file')
# NOTE: 2023-08-04
# ~/anaconda3/envs/3.11.0/lib/:~/anaconda3/envs/3.11.0/lib/python3.11/site-packages/nvidia/cudnn/lib:~/anaconda3/envs/3.11.0/lib/:~/anaconda3/envs/3.11.0/lib/python3.11/site-packages/nvidia/cudnn/lib:
# ... see bashrc and bash profile and log notes

if devices:
    print('found GPU devices:')
    print(devices)
else:
    print("TF cannot find GPU")
