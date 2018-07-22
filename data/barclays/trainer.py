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

def get_dictionary(texts, min_count=1):
    """ make corpora. texts = df.Memo_ """
    texts = list(set(texts))
    # remove words that appear only min_count times
    wc = get_word_counts(texts).sort_index()
    # if need to hash the dict for filename saving
    # or https://stackoverflow.com/questions/16589791/most-efficient-property-to-hash-for-numpy-array
    _hash = hashlib.sha1(pickle.dumps(pd.util.hash_pandas_object(wc, index=True).values)).hexdigest() # this is not stable if you don't sort above!
    filename = 'dictionary_{}.dict'.format(_hash)
    if os.path.exists(filename):
        print('reading {}'.format(filename))
        return corpora.Dictionary.load(filename)
    else:
        texts = [[token for token in text if wc[token] > min_count] for text in texts]
        dictionary = corpora.Dictionary(texts)
        print('writing {}'.format(filename))
        dictionary.save(filename)
    texts = [[token for token in text if wc[token] > min_count] for text in texts]
    dictionary = corpora.Dictionary(texts)
    return dictionary

def get_corpus(texts, dictionary):
    """
    get_corpuse(df.Memo_.unique(), dictionary)
    """
    corpus = [dictionary.doc2bow(text) for text in texts]
    # corpora.MmCorpus.serialize(filename, corpus)
    return corpus

def setup_data():
    global df, texts, dictionary, corpus, X
    df = pd.read_pickle('data.pickle')
    texts = df.Memo_.tolist()
    dictionary = get_dictionary(texts) # word encodings
    corpus = get_corpus(texts, dictionary)
    X = matutils.corpus2csc(corpus) # X.shape =  (vocabsize, ndata)

def sample_data_and_collect_responses(texts):
    texts = sorted(list(set(texts)))
    dictionary = get_dictionary()
    corpus = get_corpus(texts, dictionary)
    model = svm.LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
                    intercept_scaling=1, loss='squared_hinge', max_iter=1000,
                    multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
                    verbose=0)

flylsh = None
import flylsh

def setup_flylsh(hash_length=16, sampling_ratio=1, embedding_size=1000):
    global flylsh
    flylsh = flylsh.flylsh(X.T, hash_length, sampling_ratio, embedding_size)

try:
    df, texts, dictionary, corpus, X
except NameError as e:
    df = None
    texts = None
    dictionary = None
    corpus = None
    X = None # ~ 460 x 4000
    setup_data()
    # setup_flylsh()


if __name__ == '__main__':
    import do
    df = do.df
    texts = sorted(list(df.Memo_.unique()))
    wc = get_word_counts(texts).sort_values()
    dictionary = get_dictionary(texts)
