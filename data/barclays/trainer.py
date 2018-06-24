"""
fun finding similar things
do it yourself or copy https://radimrehurek.com/gensim/tut1.html
"""
import pandas as pd
import os
import re
from gensim import corpora
import toolz
from collections import defaultdict
import functools
import hashlib

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
    """ make corpora """
    texts = list(set(texts))
    # remove words that appear only min_count times
    wc = get_word_counts(texts).sort_values()
    # if need to hash the dict for filename saving
    _hash = hashlib.sha1(pd.util.hash_pandas_object(wc, index=True).values).hexdigest()
    filename = 'dictionary_{}.dict'.format(_hash)
    if os.path.exists(filename):
        print('reading {}'.format(filename))
        return corpora.Dictionary.load(filename)
    else:
        texts = [[token for token in text if wc[token] > min_count] for text in texts]
        dictionary = corpora.Dictionary(texts)
        print('writing {}'.format(filename))
        dictionary.save(filename)
    return dictionary

def get_corpus(texts, dictionary):
    return dictionary
