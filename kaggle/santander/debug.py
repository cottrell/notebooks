from fastFM import sgd
from numpy.random import random_integers

from fastFM.datasets import make_user_item_regression
from sklearn.cross_validation import train_test_split

# This sets up a small test dataset.
X, y, _ = make_user_item_regression(label_stdev=.4)
X_train, X_test, y_train, y_test = train_test_split(X, y)
import numpy as np
# Convert dataset to binary classification task.
y_labels = np.ones_like(y)
y_labels[y < np.mean(y)] = -1
X_train, X_test, y_train, y_test = train_test_split(X, y_labels)
print(X_train.shape, y_train.shape, X_train.dtype, y_train.dtype, type(X_train))

import scipy.sparse as ss
X_train = ss.rand(300, 40).tocsr()
y_train = random_integers(0, 1, 300) * 2.0 - 1
print(X_train.shape, y_train.shape, X_train.dtype, y_train.dtype, type(X_train))

fm = sgd.FMClassification(n_iter=1000, init_stdev=0.1, l2_reg_w=0, l2_reg_V=0, rank=2, step_size=0.1)
fm.fit(X_train, y_train)
y_pred = fm.predict(X_test)

print(y_pred)
