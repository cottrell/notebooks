from pylab import *
m = 1000
n = 1
X = zeros((m, n))
x = 5 * rand(m)
x.sort()
X[:,0] = x
f = lambda x: x ** 2
y_latent = (f(X) + 5 * randn(m, n)).sum(axis=1)
y_latent = y_latent - y_latent.mean()
y = (y_latent > 0).astype(float)
ion()
figure(1)
clf()
subplot(211)
plot(x, y_latent)

import xgboost as xgb
klf = xgb.XGBClassifier(base_score=0.5, colsample_bylevel=1,
        colsample_bytree=1, gamma=0, learning_rate=0.01, max_delta_step=0,
        max_depth=1, min_child_weight=1, missing=None, n_estimators=100,
        nthread=-1, objective='binary:logistic', reg_alpha=0, reg_lambda=1,
        scale_pos_weight=1, seed=0, silent=True, subsample=0.5)

klf.fit(X, y, early_stopping_rounds=20, eval_metric="auc", eval_set=[(X, y)])
yp = klf.predict_proba(X)

subplot(212)
plot(x, yp[:,1], 'g', alpha=0.5)
