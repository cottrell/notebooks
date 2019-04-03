from keras.backend.tensorflow_backend import set_session
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession, Session
config = ConfigProto()
config.gpu_options.allow_growth = True
config.log_device_placement = True  # to log device placement (on which device the operation ran)
# session = InteractiveSession(config=config)
import tensorflow as tf
session = tf.Session(config=config)
set_session(session)  # set this TensorFlow session as the default session for Keras
