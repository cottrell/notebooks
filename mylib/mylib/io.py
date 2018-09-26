"""
Stuff to do with reading and writing.
"""
import pandas
import re
import inspect
import pandas as pd
import numpy
import numpy as np
import gzip
import pyarrow as pa
import pyarrow.parquet as pq

def get_capped_line_count(filename, n=2):
    i = 0
    for x in _open(filename):
        i += 1
        if i >= n:
            break
    return i

def _open(filename, **kwargs):
    if filename.endswith('.gz'):
        return gzip.open(filename, **kwargs)
    else:
        return open(filename, **kwargs)

parquet_options = {'compression': 'snappy'}
def append_to_parquet_table(dataframe, filepath=None, writer=None):
    """
    Example recipe:

        writer = None
        for chunk in chunks:
            writer = append_to_parquet_table(chunk, filepath=filename, writer=writer)

    See: https://stackoverflow.com/questions/47113813/using-pyarrow-how-do-you-append-to-parquet-file
    """
    assert (filepath is not None) or (writer is not None), 'filepath and writer can not both be None'
    table = pa.Table.from_pandas(dataframe)
    if writer is None:
        writer = pq.ParquetWriter(filepath, table.schema)
    writer.write_table(table=table)
    # TODO: figure out how to preserve_index false on the append mode case
    # table = pa.Table.from_pandas(df, preserve_index=False)
    # pq.write_to_dataset(table, root_path=outfile, partition_cols=['product'], preserve_index=False)
    return writer
