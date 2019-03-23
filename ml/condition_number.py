# seems like actually is not so important to worry about condition number for learning rate
from pylab import *
ion()
import numpy as np
m = 1000
n = 10
X = np.random.randn(m, n)
i = np.argsort(X[:,-1])
X = X[i,:]
X = X - np.mean(X) # must be mean centered other wise nothing works well
theta = 0.8
for i in range(3):
    X[:,0] = X[:,-1] * theta + (1 - theta) * X[:,i]


y = X[:,-1] + 0.0 * np.random.randn(m)

S = np.corrcoef(X.T)

# print(np.linalg.cond(X))
print(np.linalg.cond(S))
# print(np.linalg.matrix_rank(X))


import tensorflow as tf
import tensorflow.keras as keras

lr = 0.01
model = keras.models.Sequential([
    keras.layers.Dense(8),
    keras.layers.LeakyReLU(),
    keras.layers.Dense(8),
    keras.layers.LeakyReLU(),
    keras.layers.Dense(8),
    keras.layers.LeakyReLU(),
    keras.layers.Dense(8),
    keras.layers.LeakyReLU(),
    keras.layers.Dense(1)])
model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), loss=keras.losses.MSE)

l = model.fit(X, y, epochs=10, verbose=0)
figure(1)
clf()
plot(l.history['loss'])
show()

figure(2)
clf()
subplot(3,1,1)
x = X[:,-1]
yp = model.predict(X).squeeze()
plot(x, y)
plot(x, yp)
subplot(3, 1, 2)
err = yp - y
ylabel('err')
plot(x, err)
subplot(3, 1, 3)
plot(x, err / y)
ylabel('rel err')
tight_layout()
show()
