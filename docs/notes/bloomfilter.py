# Are bloom filters consistent?
import random
import bloom_filter
import pandas as pd

n_train_0 = 1000
n_train_1 = 100
n_test = 1000

# create unique data
data = set()
while len(data) < (n_train_0 + n_train_1 + n_test):
    data.add(random.getrandbits(128))

data = list(data)
data_train_0 = data[:n_train_0]
data_train_1 = data[n_train_0:(n_train_0 + n_train_1)]
data_test = data[(n_train_0 + n_train_1):] # we will not add these so they should all be truly false or falsely true.

bf = bloom_filter.BloomFilter(max_elements=1000, error_rate=0.1, start_fresh=True)
# add some in case there is a switch that always returns zero when empty
for x in data_train_0:
    bf.add(x)
# check results before adding
df = pd.DataFrame(index=data_test)
df["before"] = [x in bf for x in data_test]
for x in data_train_1:
    bf.add(x)
df["after"] = [x in bf for x in data_test]

# I think there are no True"s becoming False ?
print(df.drop_duplicates())

# In [105]: import bloomfilter as b; b.df.drop_duplicates()
# Out[105]:
#                                          before  after
# 111044130385193285289821201715410235957    True   True
# 239224036934766132926441231327779608901   False   True
# 252668175872275653764385314979389915789   False  False
