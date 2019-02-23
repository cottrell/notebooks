import pandas as pd
import os
import time

t0 = time.time()
print("reading file ./DeathRecords.csv")
df = pd.read_csv('./DeathRecords.csv', nrows=None, header=0)

for k in df.columns[1:]: # skip Id
    filename = '{}.csv'.format(k)
    if os.path.exists(filename):
        d = pd.read_csv(filename, header=0)
        d = d.set_index('Code')['Description']
        # could be faster also create codes, categories but this involves less worry
        print('mapping {}: {} shape={}'.format(k, filename, d.shape))
        df[k] = df[k].map(d)
    else:
        print('{} dne. skipping'.format(filename))
    df[k] = df[k].astype('category')

df = df.drop('Id', axis=1)

# outfile = 'DeathRecords.hdf'
# print('saving {}'.format(outfile))
# df.to_hdf(outfile, 'data', mode='w')
import bc
outfile = 'DeathRecords.carrays'
print('saving {}'.format(outfile))
bc.to_carrays(df, outfile)
print('{} seconds'.format(time.time() - t0))
