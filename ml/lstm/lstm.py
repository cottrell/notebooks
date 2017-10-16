#!/usr/bin/env python
import bcolz
import pandas as pd
import os
import time
import numpy.random as nr
import numpy as np
import tensorflow as tf
import tensorflow.contrib.keras as K
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.layers.wrappers import TimeDistributed
from cached import get_data
mydir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(mydir, '../../data/bis/all.text')

def run(filename=filename,
        batch_size=50,
        layer_num=2,
        seq_length=50,
        hidden_dim=500,
        generate_length=500,
        nb_epoch=20,
        mode='train',
        weights=''):
    X, y, vocab_size, ix_to_char = load_data(seq_length)

    # Creating and compiling the Network
    model = Sequential()
    model.add(LSTM(hidden_dim, input_shape=(None, vocab_size), return_sequences=True))
    for i in range(layer_num - 1):
        model.add(LSTM(hidden_dim, return_sequences=True))
    model.add(TimeDistributed(Dense(vocab_size)))
    model.add(Activation('softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

    # Generate some sample before training to know how bad it is!
    generate_text(model, generate_length, vocab_size, ix_to_char)

    if not weights == '':
        model.load_weights(weights)
        nb_epoch = int(weights[weights.rfind('_') + 1:weights.find('.')])
    else:
        nb_epoch = 0

    # Training if there is no trained weights specified
    if mode == 'train' or weights == '':
        while True:
            print('\n\nEpoch: {}\n'.format(nb_epoch))
            model.fit(X, y, batch_size=batch_size, verbose=1, nb_epoch=1)
            nb_epoch += 1
            generate_text(model, generate_length, vocab_size, ix_to_char)
            if nb_epoch % 10 == 0:
                model.save_weights('checkpoint_layer_{}_hidden_{}_epoch_{}.hdf5'.format(layer_num, hidden_dim, nb_epoch))

    # Else, loading the trained weights and performing generation only
    elif weights == '':
        # Loading the trained weights
        model.load_weights(weights)
        generate_text(model, generate_length, vocab_size, ix_to_char)
        print('\n\n')
    else:
        print('\n\nNothing to do!')


def build_model(m_input=128, n_input=32):
    # build the model: a single LSTM
    print('Build model...')
    model = K.models.Sequential()
    model.add(K.layers.LSTM(128, input_shape=(m_input, n_input)))
    model.add(K.layers.Dense(n_input))
    model.add(K.layers.Activation('linear'))
    optimizer = K.optimizers.RMSprop(lr=0.01)
    start = time.time()
    model.compile(loss='mse', optimizer=optimizer)
    print("> Compilation Time : ", time.time() - start)
    return model

def load_data(seq_length, filename=filename, maxlen=10000):
    data, chars, vocab_size = get_data(filename=filename, maxlen=10000)
    # chars is ints: ord('a') is chr(97)
    print('Data length: {} characters'.format(len(data)))
    print('Vocabulary size: {} characters'.format(vocab_size))

    ix_to_char = {ix: char for ix, char in enumerate(chars)}
    char_to_ix = {char: ix for ix, char in enumerate(chars)}
    xfile = os.path.join(mydir, 'X_{}_{}.bcolz'.format(seq_length, maxlen))
    yfile = os.path.join(mydir, 'y_{}_{}.bcolz'.format(seq_length, maxlen))
    if os.path.exists(xfile):
        print('using cached values from {}'.format(xfile))
        X = bcolz.carray(rootdir=xfile, mode='r')[:]
        y = bcolz.carray(rootdir=yfile, mode='r')[:]
        return X, y, vocab_size, ix_to_char
    else:
        print('no file {}'.format(xfile))
    # 6 s
    print('mapping data')
    data_mapped = np.array(list(map(char_to_ix.get, data)))

    nnn = int(len(data_mapped) / seq_length)
    print('nnn = {}'.format(nnn))

    X = np.zeros((nnn, seq_length, vocab_size), dtype=np.int16)
    y = np.zeros((nnn, seq_length, vocab_size), dtype=np.int16)
    I = np.eye(vocab_size, dtype=np.int16)
    t0 = time.time()
    for i in range(0, nnn):
        if i % 100 == 1:
            percent_done = i / float(nnn)
            eta = (1 - percent_done) * (time.time() - t0) / percent_done / 60
            print('iteration {}: {} done. ETA {} minutes'.format(i, percent_done, eta))
        X[i] = I[data_mapped[i * seq_length:(i+1) * seq_length]]
        y[i] = I[data_mapped[i * seq_length + 1:(i+1) * seq_length + 1]]

    print('saving bcolz')
    bcolz.carray(X, rootdir=xfile)
    bcolz.carray(y, rootdir=yfile)
    return X, y, vocab_size, ix_to_char

def generate_text(model, length, vocab_size, ix_to_char):
    # starting with random character
    ix = [np.random.randint(vocab_size)]
    y_char = [ix_to_char[ix[-1]]]
    X = np.zeros((1, length, vocab_size))
    for i in range(length):
        # appending the last predicted character to sequence
        X[0, i, :][ix[-1]] = 1
        print(ix_to_char[ix[-1]], end="")
        ix = np.argmax(model.predict(X[:, :i + 1, :])[0], 1)
        y_char.append(ix_to_char[ix[-1]])
    return ('').join(y_char)

if __name__ == '__main__':
    import argh
    argh.dispatch_command(run)
