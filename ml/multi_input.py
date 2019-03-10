# pip install tf-nightly-gpu
import tensorflow as tf
import tensorflow.keras.activations as ka
import tensorflow.keras.backend as K
import tensorflow.keras.layers as kl
import tensorflow.keras.models as km
import numpy as np

class Model(km.Model):
    def __init__(self, dim, z_dim=9):
        self._z_grid = np.linspace(-1, 1, z_dim)
        X_input = kl.Input(shape=(None, dim))
        Z_input = kl.Input(shape=(None, None, 1))
        super().__init__()
        self.dim = dim
    # def call(self, inputs):
    #     return self.call_with_z([inputs, self._z_grid])
    def call(self, inputs):
        X, Z = inputs
        X_layer = kl.Dense(16, activation='linear')(X)
        Z_dense = kl.Dense(16, activation='linear')
        combined = list()
        for i in range(Z.shape[-1]):
            z = Z_dense(Z[:,i])
            l = X_layer + z
            l = K.expand_dims(l, axis=1)
            combined.append(l)
        combined = kl.concatenate(combined, axis=1)
        # combined is now shape (batch_size, z_size, 16)
        l = ka.relu(combined)
        l = kl.Dense(16, activation='relu')(l)
        l = kl.Dense(16, activation='relu')(l)
        main_output = kl.Dense(1, activation='linear')(l)
        return main_output

dim = 6
m = 100
X = np.random.randn(m, dim)
Z = np.random.randn(1, 10)

model = Model(dim)

out = model.predict([X, Z])
# out = model.predict(X.head().values)


# 
# import my.extractors as e
# df_ = e.pdr.get_yahoo_price_volume.load([('symbol', '=', 'ibm')])
# 
# def mangle_enrich(df):
#     df = df.set_index('date').sort_index()
#     # assume everything is adjusted properly for splits
#     df = df.rename(columns={'adj close': 'adj_close'})
#     adj_factor = df['adj_close'] / df['close']
#     for k in ['high', 'low', 'open']:
#         df[k] = df[k] * adj_factor
#     df = df.drop('close', axis=1)
#     # df['dt'] = df.index.to_series().diff().dt.days
#     df['t'] = (df.index.to_series() - df.index.min()).dt.days
#     for lag in [1, 2, 5]: # , 10, 15, 20]:
#         lag_close = df['adj_close'].shift(lag)
#         for k in ['high', 'low', 'open', 'adj_close']:
#             kk = f'r_{lag}_{k}'
#             df[kk] = df[k] / lag_close - 1
#         df[f'r_{lag}_t'] = df['t'] - df['t'].shift(lag)
#     df = df.drop(['high', 'low', 'open', 'adj_close', 'product', 'symbol', 't'], axis=1)
#     for k in ['dividends', 'splits']:
#         df[k] = df[k].fillna(0)
#     # df = df.dropna()
#     out = list()
#     df['target'] = df['r_1_adj_close'].shift(-1)
#     return df
# 
# df_ = mangle_enrich(df_)
# 
# date = '2018-01-01'
# df, df_test = df_.loc[:date], df_.loc[date:]
# print(df.shape, df_test.shape)
# 
# xcols = [x for x in df.columns if x != 'target']
# ycols = ['target']
# 
# X = df[xcols]
# y = df[ycols]



# dim = X.shape[1]

