#!/usr/bin/env python3
# if version.parse(tf.__version__).release[0] >= 2:
# THIS SEEMS TO WORK IN BOTH tf 2 and 1
from packaging import version
import tensorflow as tf
from tensorflow.keras.backend import set_session
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession, Session
config = ConfigProto()
config.gpu_options.allow_growth = True
config.log_device_placement = True  # to log device placement (on which device the operation ran)
# session = InteractiveSession(config=config)
import tensorflow as tf
session = Session(config=config)
set_session(session)  # set this TensorFlow session as the default session for Keras


import tensorflow.keras as keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import Flatten,  MaxPooling2D, Conv2D
from tensorflow.keras.callbacks import TensorBoard

(X_train,y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000,28,28,1).astype('float32')
X_test = X_test.reshape(10000,28,28,1).astype('float32')

X_train /= 255
X_test /= 255

n_classes = 10
y_train = keras.utils.to_categorical(y_train, n_classes)
y_test = keras.utils.to_categorical(y_test, n_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(28,28,1)) )
model.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(n_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# tensor_board = TensorBoard('/tmp/LeNet-MNIST-1')

model.fit(X_train, y_train, batch_size=128, epochs=15, verbose=1, validation_data=(X_test,y_test)) # , callbacks=[tensor_board])

