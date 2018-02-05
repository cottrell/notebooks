#!/usr/bin/env python
import numpy as np
import nltk
import datetime
import numpy.random
import sys
import gzip
import pandas as pd
import re
import glob
import os
import argh

mydir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(mydir, 'all.text')
filename_mangled = os.path.join(mydir, 'mangled.text.gz')

def get_files():
    return glob.glob(os.path.join(mydir, 'text/*.text'))

# do something dumb to try to detect good paragraphs
def sample_generator(n=20):
    outdir = os.path.join(mydir, 'paragraphs')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    filenames = get_files()
    data = list()
    while True:
        filename = numpy.random.choice(filenames)
        print(filename)
        d = re.split('\n{2,}', open(filename).read().strip())
        for x in numpy.random.choice(d, min(n, len(d)), replace=False):
            yield x

# do something dumb to try to detect good paragraphs
def sample_paragraphs_collect_responses(n=10, learning_rate=0.1):
    outdir = os.path.join(mydir, 'paragraphs')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    filenames = get_files()
    data = list()
    # accept sample at 2 * obs rate
    alpha = 0.5
    for i, x in enumerate(sample_generator()):
        # TODO predict and check
        # assert res in ['y', 'n']
        if i % 10 == 0:
            l = train_paragraphs() # TODO warm, re-use
            model = l['model']
        pred = model.predict(np.array([get_features(x)]))
        pred = 'y' if pred == 1 else 'n'
        r = numpy.random.rand()
        theta = alpha if pred == 'y' else 1 - alpha
        if r < theta:
            print('skipping this one ({}, theta={}, model={}): {}'.format(r, theta, pred, x))
            continue
        else:
            print('not skipping this one ({}, theta={}, model={}): {}'.format(r, theta, pred, x))

        print('\nModel says {}'.format(pred))
        print('')
        print(x)
        print('')
        res = None
        while res not in ['y', 'n', 'q']:
            res = input('is this good? y or n [q to quit]')
        if res == 'q':
            break
        alpha = alpha * (1 - learning_rate) + learning_rate * (2 * (res == 'y') - 1)
        alpha = min(1, max(0, alpha))
        print('\nalpha {}\n'.format(alpha))
        data.append([res, x])
    filename = os.path.join(outdir, datetime.datetime.today().isoformat())
    print('writing {}'.format(filename))
    df = pd.DataFrame(data, columns=['y', 'x'])
    df.to_csv(filename, index=False)

_feature_columns = ['n', 'nn']
def get_features(x):
    def token_etc(x):
        x = nltk.tokenize.wordpunct_tokenize(re.sub('\W', ' ', x))
        return x
    return [len(x), len(token_etc(x))]

def get_paragraph_data():
    files = glob.glob(os.path.join(mydir, 'paragraphs/*'))
    df = pd.concat([pd.read_csv(f, dtype=str) for f in files])
    df.index = range(df.shape[0]) # otherwise problems with non-uniques
    df['x'] = df.x.astype(str)
    _f = pd.DataFrame([get_features(x) for x in df.x.values], columns=_feature_columns)
    df = pd.concat([df, _f], axis=1)
    df['y'] = np.where(df.y.values == 'y', 1, 0)
    from sklearn import model_selection
    df_train, df_test = model_selection.train_test_split(df)
    return df_train, df_test

def train_paragraphs():
    df_train, df_test = get_paragraph_data()
    import sklearn.linear_model as lm
    model = lm.LogisticRegression(C=1000.0, class_weight='balanced', dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)
    xcol = ['n', 'nn']
    ycol = ['y']
    model.fit(df_train[xcol], df_train[ycol].squeeze())
    ypred_train = model.predict(df_train[xcol])
    ypred = model.predict(df_test[xcol])
    ytrue_train = df_train[ycol].values.squeeze()
    ytrue = df_test[ycol].values.squeeze()
    c = pd.DataFrame([ytrue, ypred]).T
    c.columns = ['true', 'pred']
    import sklearn.metrics as sm
    print('train auc:', sm.roc_auc_score(ytrue_train, ypred_train))
    print('test  auc:', sm.roc_auc_score(ytrue, ypred))
    print('confusion train:\n', sm.confusion_matrix(ytrue_train, ypred_train))
    print('confusion:\n', sm.confusion_matrix(ytrue, ypred))
    return locals()

def process_file(f):
    # fout = open(filename, 'w')
    # reg = re.compile('\.{2,}')
    reg = re.compile('[^a-zA-Z]')
    print('file {}'.format(f))
    for line in open(f):
        line = reg.sub(' ', line).strip()
        print(len(line))
        if len(line) > 10:
            yield line
            # fout.write(line)
    # fout.write('\n')
    # os.system('gzip -f {}'.format(filename))

def mangle(filename=filename + '.gz', outfile=filename_mangled):
    """ preprocessing only, do this once (manually) basically """
    if sys.version_info[0] < 3:
        raise Exception('python 2 not work')
    print('reading {}'.format(filename))
    data = gzip.open(filename).read().decode('utf-8')
    # 12 s
    s = pd.Series(list(data)).value_counts()
    # 6 s
    # keep chars with more than 1000 occurences
    a = str.maketrans({k: ' ' for k in s[s<1000].index.tolist()})
    data = data.translate(a)
    print('writing {}'.format(outfile))
    gzip.open(outfile, 'w').write(data.encode())

if __name__ == '__main__':
    argh.dispatch_commands([make, mangle])
