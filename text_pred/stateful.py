import numpy as np
N_train = 1000
n_dim = 20
from numpy.random import choice, randn
one_indexes = choice(a=N_train, size=int(N_train / 2), replace=False)
X_train = randn(N_train, n_dim)
X_train[one_indexes, 0] = 1  # very long term memory.
y_train = randn(N_train)

def prepare_sequences(x_train, y_train, window_length):
    windows = []
    windows_y = []
    for i, sequence in enumerate(x_train):
        len_seq = len(sequence)
        for window_start in range(0, len_seq - window_length + 1):
            window_end = window_start + window_length
            window = sequence[window_start:window_end]
            windows.append(window)
            windows_y.append(y_train[i])
    return np.array(windows), np.array(windows_y)

a, b = prepare_sequences(X_train, y_train, 10)
print(X_train.shape, y_train.shape, a.shape, b.shape)

# print('Building STATELESS model...')
# model = Sequential()
# model.add(LSTM(10, input_shape=(max_len, 1), return_sequences=False, stateful=False))
# model.add(Dense(1, activation='sigmoid'))
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=15, validation_data=(X_test, y_test), shuffle=False)
# score, acc = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
