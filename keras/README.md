Just reminders and notes.

import keras as K
from keras.layers import Dense
from keras import Sequential
model = Sequential()
model.add(Dense(32, activation='relu', input_shape=[100]))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

import numpy as np
data = np.random.random((1000, 100))
labels = np.random.randint(2, size=(1000, 1))

model.fit(data, labels, epochs=10, batch_size=32)
