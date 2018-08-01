# https://getstream.io/blog/factorization-recommendation-systems/
# blog hard to read without the data shown
import pandas as pd
from collections import Counter
import tensorflow as tf
from tffm import TFFMRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

# Loading datasets'

buys = open('yoochoose-buys.dat', 'r')
clicks = open('yoochoose-clicks.dat', 'r')

initial_buys_df = pd.read_csv(buys, names=['Session ID', 'Timestamp', 'Item ID', 'Category', 'Quantity'],
                              dtype={'Session ID': 'float32', 'Timestamp': 'str', 'Item ID': 'float32',
                                     'Category': 'str'})

initial_buys_df.set_index('Session ID', inplace=True)

initial_clicks_df = pd.read_csv(clicks, names=['Session ID', 'Timestamp', 'Item ID', 'Category'],
                                dtype={'Category': 'str'})

initial_clicks_df.set_index('Session ID', inplace=True)

# We won't use timestamps in this example

initial_buys_df = initial_buys_df.drop('Timestamp', 1)
initial_clicks_df = initial_clicks_df.drop('Timestamp', 1)

# For illustrative purposes, we will only use a subset of the data: top 10000 buying users,

x = Counter(initial_buys_df.index).most_common(10000)
top_k = dict(x).keys()
initial_buys_df = initial_buys_df[initial_buys_df.index.isin(top_k)]
initial_clicks_df = initial_clicks_df[initial_clicks_df.index.isin(top_k)]

# Create a copy of the index, since we will also apply one-hot encoding on the index

initial_buys_df['_Session ID'] = initial_buys_df.index
