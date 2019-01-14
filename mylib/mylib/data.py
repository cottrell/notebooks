import string
import functools
import pandas as pd
import random
from numpy.random import rand, randint
import logging
from . import tools

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

def _get_accuracies(df, cola, colb):
    print('check {} {}'.format(cola, colb))
    s = df.groupby([cola, colb]).size().reset_index()
    s.columns = [cola, colb, 'size']
    s = s.sort_values('size')
    g = s.groupby(cola)['size']
    a = g.last() / g.sum() # take largest by size as "correct"
    g = s.groupby(colb)['size']
    b = g.last() / g.sum() # take largest by size as "correct"
    ma = a.mean()
    mb = b.mean()
    return cola, colb, ma, mb

def _check_hashable(d, cols):
    dd = d.drop_duplicates(cols).copy()
    dd['h'] = pd.util.hash_pandas_object(dd, index=False)
    assert dd.h.value_counts().max() == 1

from itertools import chain, combinations

def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def _do_groupby_size(df, cols):
    # first thing you try before going to GAN, LDA or whatever
    # TODO: might want laplace smooth etc
    if len(cols) > 1:
        _check_hashable(df, cols)
        h = pd.util.hash_pandas_object(df[cols], index=False)
        s = df.groupby(h).size()
        s = s / s.sum()
        return cols, h.map(s)
    s = df.groupby(cols).size()
    s = s / s.sum()
    return cols, df[cols[0]].map(s)

def basic_multinomial_naive_bayes_counter_across_all_features(df, cols, thresh=0.9, colprefix=None):
    """ groupby size across all feature subset """
    tasks = list()
    for subset in powerset(cols):
        if len(subset) > 0:
            print('getting {}'.format(subset))
            task = functools.partial(_do_groupby_size, df, list(subset))
            tasks.append(task)
    res = tools.run_tasks_in_parallel(*tasks, max_workers=40)
    r = [x['result'] for x in res]
    d = pd.concat([x[1] for x in r], axis=1)
    d.columns = ['_'.join(x[0]) for x in r]
    if colprefix is not None:
        d.columns = ['{}{}'.format(colprefix, x) for x in d.columns]
    return d


def discover_feature_hierarchy_in_df(df, cols, thresh=0.9):
    """
    Try to establish a hierachy between the features. For example, detect that county -> district -> town.

    TODO: do more with the relative accuracies. This was just a quick hack. Use the dataframe "d" for complete bidirectional edges information.
    """
    tasks = list()
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            task = functools.partial(_get_accuracies, df, cols[i], cols[j])
            tasks.append(task)
    res = tools.run_tasks_in_parallel(*tasks, max_workers=20)
    r = [x['result'] for x in res]
    edges = list()
    for x in r:
        edges.append((x[0], x[1], x[2]))
        edges.append((x[1], x[0], x[3]))
    edges = [x for x in edges if x[2] >= thresh]
    d = pd.DataFrame(r, columns=['a', 'b', 'ma', 'mb'])
    return edges, d

def plot_transitive_reduction_of_condensation(edges):
    """ plot something from discover_feature_hierarchy_in_df """
    import networkx as nx
    g = nx.DiGraph()
    for x in edges:
        g.add_edge(x[0], x[1], weight=x[2])
    gg = nx.condensation(g)
    mapping = {i: '\n'.join(gg.nodes[i]['members']) for i in range(len(gg.nodes))}
    ggg = nx.relabel.relabel_nodes(gg, mapping)
    gggg = nx.transitive_reduction(ggg)
    import matplotlib.pyplot as plt
    plt.clf()
    plt.ion()
    plt.subplot(211)
    nx.draw_networkx(ggg)
    plt.subplot(212)
    nx.draw_networkx(gggg)
    plt.tight_layout()
    plt.show()
    return gggg
