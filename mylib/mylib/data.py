import string
import random
from numpy.random import rand, randint
import logging

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def obscure_df_inplace(df, str_len=8):
    for k in df.columns:
        dtype_name = df[k].dtype.name
        if dtype_name == 'category' and df[k].cat.categories.dtype.name == 'object':
            # maybe strings in cats, could check types of objects but this is safer
            new_categories = [id_generator(str_len) for x in range(len(df[k].cat.categories))]
            df[k].cat.rename_categories(new_categories, inplace=True)
        elif dtype_name == 'object':
            categories = df[k].unique()
            new_categories = [id_generator(str_len) for x in range(len(categories))]
            # will fail if objects are not str, this is intentional
            d = dict(zip(categories, new_categories))
            df[k] = df[k].map(d).values # values to avoid index align
        elif dtype_name.startswith('float'):
            m = df[k].min()
            M = df[k].max()
            df[k] = (M - m) * rand(df[k].shape[0]) + m
        elif dtype_name.startswith('int') or dtype_name.startswith('uint'):
            m = df[k].min()
            M = df[k].max()
            df[k] = randint(m, M, df[k].shape[0])
        else:
            logging.warning('not obscuring column {} type is {}'.format(k, dtype_name))
            continue
        df[k] = df[k].astype(dtype_name)

def iris():
    import pandas
    import sklearn.datasets as datasets
    d = datasets.load_iris()
    c = pandas.Categorical.from_codes(d.target, d.target_names)
    df = pandas.DataFrame(d.data, columns=d.feature_names)
    df['name'] = c
    df = df.sort_index(axis=1)
    dfd = pandas.get_dummies(df)
    return df, dfd
