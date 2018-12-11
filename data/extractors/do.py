#!/usr/bin/env python
import pandas_datareader as pdr
import pandas_datareader.fred as fred
import os

_data_dir = os.path.join(os.path.expanduser('~/projects/data'))

if not os.path.exists(_data_dir):
    os.makedirs(_data_dir)

# utils
import pyarrow as pa
import pyarrow.parquet as pq
def write_parquet(df, filename, partition_cols=None, preseve_index=False):
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_to_dataset(table, root_path=filename, partition_cols=partition_cols, preserve_index=preserve_index)
# notes: you need all of this to use joblib and get the filename before calling! what is joblib actually missing if you simply return the location of the CACHED file?
# pdr.memory.cached_requests_get.store_backend.location
# _, args_id, metadata = pdr.memory.cached_requests_get._cached_call(('http://www.google.com',), {})
# args_id
# In [38]: joblib.memory._build_func_identifier(pdr.memory.cached_requests_get)
# Out[38]: 'pandas_datareader/memory/cached_requests_get'

# YES, that might be the right pattern to hijack joblib: extractors simply return the cached filename without loading it? Does that involve changing joblib?

# impure function pattern
# joblib.hash(df) : data_hash where data is stored, consider bucketing to avoid ls bombs. You should not be ls-ing this anyway.
# joblib.func_inspect.get_func_name OR joblib.memory._build_func_identifier(fun) # func_name (rough) IGNORE NAME? DO YOU WANT A RENAME TO FORCE RERUNS?
#
# joblib.func_inspect.get_func_code(fun) : code # has func name in it
# args

# In [67]: pdr.memory.cached_requests_get._get_output_identifiers(url)
# Out[67]: ('pandas_datareader/memory/cached_requests_get', '9bfe189d9b33cbe8965991a1d0a77227')

# In [69]: pdr.memory.cached_requests_get.store_backend.contains_item(('pandas_datareader/memory/cached_requests_get', '9bfe189d9b33cbe8965991a1d0a77227'))
# Out[69]: True


def something(x, a=1):
    print(a)
    return x, a


def get_fred_tag_rate_daily():
    df = fred.get_series_by_tag('rate,daily')
