"""
fun finding similar things
do it yourself or copy https://radimrehurek.com/gensim/tut1.html
"""
import pandas as pd
import os
import re
from gensim import corpora, matutils # matutils.corpus2csc, corpus2dense
import toolz
from collections import defaultdict
import functools
import hashlib
import sklearn.svm
import pickle

def sub_chainer(subs):
    """ chain regex subs """
    subs = [(re.compile(x), y)  for x, y in subs[::-1]] # reverse
    funcs = list()
    for reg, y in subs:
        f = functools.partial(reg.sub, y)
        funcs.append(f)
    return toolz.compose(*funcs)

subs = [
        # ('[0-9]', '9'),
        ('\W*ON\W(\d\d\W[A-Z]{3})\W*', ' ONDATE '),
        ('\W*FOR PERIOD\W*[0-9A-Z]{4,5}/\W*[0-9A-Z]{4,5}', ' FORPERIOD '),
        ('[^a-zA-Z0-9]', ' '),
        ]
fsub = sub_chainer(subs)

def preproc_docs(documents):
    stoplist = []
    texts = [fsub(document).lower() for document in documents]
    texts = [tuple([word.strip() for word in text.split() if word not in stoplist]) for text in texts]
    return documents, texts

def get_word_counts(texts):
    return pd.Series([token for text in texts for token in text]).value_counts()

def get_dictionary(texts, min_count=2):
    """ make corpora. texts = df.Memo_ """
    texts = list(set(texts))
    # for words that appear only min_count times, replace them with OTHER
    wc = get_word_counts(texts).sort_index()
    # if need to hash the dict for filename saving
    # or https://stackoverflow.com/questions/16589791/most-efficient-property-to-hash-for-numpy-array
    _hash = hashlib.sha1(pickle.dumps(pd.util.hash_pandas_object(wc, index=True).values)).hexdigest() # this is not stable if you don't sort above!
    filename = 'dictionary_{}.dict'.format(_hash)
    texts = [[token if wc[token] >= min_count else 'OTHER' for token in text] for text in texts]
    texts = list(set([tuple(x) for x in texts]))
    if os.path.exists(filename):
        print('reading {}'.format(filename))
        return texts, corpora.Dictionary.load(filename)
    else:
        dictionary = corpora.Dictionary(texts)
        print('writing {}'.format(filename))
        dictionary.save(filename)
    return texts, dictionary

def get_corpus(texts, dictionary):
    """ get_corpuse(df.Memo_.unique(), dictionary) """
    corpus = [dictionary.doc2bow(text) for text in texts]
    # corpora.MmCorpus.serialize(filename, corpus)
    return corpus

def setup_data():
    global df, texts, texts_mod, dictionary, corpus, X
    df = pd.read_pickle('data.pickle')
    texts = list(set(df.Memo_.tolist()))
    texts_mod, dictionary = get_dictionary(texts) # word encodings
    corpus = get_corpus(texts_mod, dictionary)
    X = matutils.corpus2csc(corpus) # X.shape =  (vocabsize, ndata)

# def sample_data_and_collect_responses(texts):
#     texts = sorted(list(set(texts)))
#     dictionary = get_dictionary()
#     corpus = get_corpus(texts_mod, dictionary)
#     model = svm.LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
#                     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
#                     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
#                     verbose=0)

import flylsh

_hash_length = 64
def setup_flylsh(hash_length=_hash_length, sampling_ratio=0.3, embedding_size=None):
    global lsh
    if embedding_size is None:
        embedding_size = X.T.shape[1] * 40 # i.e. 50 into 2000
    lsh = flylsh.flylsh(X.T, hash_length, sampling_ratio, embedding_size)

def query(n=None, n_neighbours=3):
    if n is None:
        n = len(texts_mod)
    d = list()
    for i in range(n):
        print('{} of {}'.format(i, n))
        temp = lsh.query(i, n_neighbours)
        temp = [texts_mod[i]] + [texts_mod[x] for x in temp]
        print(temp)
        d.append(temp)
    return d

try:
    df, texts, texts_mod, dictionary, corpus, X, lsh
except NameError as e:
    lsh = None
    df = None
    texts = None
    texts_mod = None
    dictionary = None
    corpus = None
    X = None # ~ 460 x 4000
    # setup_data()
    # setup_flylsh()

if __name__ == '__main__':
    import do
    df = do.df
    texts = sorted(list(df.Memo_.unique()))
    wc = get_word_counts(texts).sort_values()
    dictionary = get_dictionary(texts)
