import re
import nltk
import os
txt_orig = open(os.path.expanduser('~/Downloads/out.txt')).read()
pattern = re.compile('^[\W_]*')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
a = tokenizer.tokenize(txt)
a = [pattern.sub('', x).strip() for x in a]
pattern = re.compile('^[A-Z ]*\n*')
a = [pattern.sub('', x).strip() for x in a]

