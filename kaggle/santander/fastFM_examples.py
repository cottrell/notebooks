from fastFM.datasets import make_user_item_regression
from sklearn.cross_validation import train_test_split

# This sets up a small test dataset.
X, y, _ = make_user_item_regression(label_stdev=.4)
X_train, X_test, y_train, y_test = train_test_split(X, y)

from fastFM import als
fm = als.FMRegression(n_iter=1000, init_stdev=0.1, rank=2, l2_reg_w=0.1, l2_reg_V=0.5)
fm.fit(X_train, y_train)
y_pred = fm.predict(X_test)

from sklearn.metrics import mean_squared_error
print('mse:', mean_squared_error(y_test, y_pred))

import numpy as np
# Convert dataset to binary classification task.
y_labels = np.ones_like(y)
y_labels[y < np.mean(y)] = -1
X_train, X_test, y_train, y_test = train_test_split(X, y_labels)

from fastFM import sgd
fm = sgd.FMClassification(n_iter=1000, init_stdev=0.1, l2_reg_w=0,
                          l2_reg_V=0, rank=2, step_size=0.1)
fm.fit(X_train, y_train)
y_pred = fm.predict(X_test)

y_pred_proba = fm.predict_proba(X_test)

from sklearn.metrics import accuracy_score, roc_auc_score
print('acc:', accuracy_score(y_test, y_pred))
print('auc:', roc_auc_score(y_test, y_pred_proba))

from fastFM import mcmc
fm = mcmc.FMClassification(n_iter=1000, rank=2, init_stdev=0.1)

y_pred = fm.fit_predict(X_train, y_train, X_test)
y_pred_proba = fm.fit_predict_proba(X_train, y_train, X_test)

from sklearn.metrics import accuracy_score, roc_auc_score
print('acc:', accuracy_score(y_test, y_pred))
print('auc:', roc_auc_score(y_test, y_pred_proba))

