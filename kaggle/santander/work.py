from dataprep import *

df = train

X = train[xcols].values
y = train[ycol].values
m, n = X.shape

Xtest = d['test'][xcols]

print('y sparsity {}'.format((y == 0).sum() / float(m)))
print('X sparsity {}'.format((X == 0).sum().sum() / float(np.prod(X.shape))))
print('X test sparsity {}'.format((Xtest == 0).sum().sum() / float(np.prod(Xtest.shape))))


import sklearn.ensemble as se
import sklearn.linear_model as lm
import sklearn.preprocessing as preprocessing
import sklearn.metrics as metrics
import sklearn.decomposition as decomposition
import sklearn.cross_validation as cross_validation

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3)

Xt = X_train.copy()
# Xt = decomposition.PCA(n_components=10).fit_transform(Xt)
ss = preprocessing.StandardScaler(copy=True, with_mean=True, with_std=True).fit(Xt)
Xt = ss.transform(Xt)
X_test = ss.transform(X_test)
# e = lm.RidgeClassifier(alpha=0.1, class_weight=None, copy_X=True, fit_intercept=True, max_iter=None, normalize=False, random_state=None, solver='auto', tol=0.001)
e = se.ExtraTreesClassifier(bootstrap=False, class_weight=None,
        criterion='gini', max_depth=None, max_features='auto',
        max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1, oob_score=False, random_state=None, verbose=0, warm_start=False)
e.fit(Xt, y_train)
for k, x, y in zip(['train', 'test'], [Xt, X_test], [y_train, y_test]):
    pred = e.predict(x)
    fpr, tpr, thresholds = metrics.roc_curve(y, pred)
    auc = metrics.auc(fpr, tpr)
    print(k, auc)

def get_num_components(splain=0.999):
    u, d, v = svd(X.values)
    dd = d ** 2
    s = 1 - dd.cumsum() / dd.sum()
    i = find(s > splain)
    return i[0]



# def get_feature_importances():
#     e = se.ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='gini', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=1, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1, oob_score=False, random_state=None, verbose=1, warm_start=False)
#     e.fit(X, y)
#     return e
# 
# # def save_data(d):
#     for k in d:
#         print('writing {}'.format(k))
#         bc.to_carrays(d[k], k)
