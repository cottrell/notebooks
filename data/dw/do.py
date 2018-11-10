import pandas as pd
import datadotworld as dw
d = dw.load_dataset('ian/3-centuries-of-uk-economy-data') # pull data into ~/.dw
s = pd.Series({k: v.shape for k, v in d.dataframes.items()})

df_orig = d.dataframes['m6_mthly_prices_and_wages']
cols = df_orig.iloc[1:5]
names = cols.iloc[:,0].values
cols = pd.MultiIndex.from_arrays(cols.iloc[:,2:].values)
cols.names = names

df = df_orig.iloc[5:].set_index(['column_a', 'column_b'])
df.index.names = ['year', 'month']
df.columns = cols
df = df.astype(float)
