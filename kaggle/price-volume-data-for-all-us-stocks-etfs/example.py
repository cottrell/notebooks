import os
import pandas as pd
_mydir = os.path.dirname(os.path.realpath(__file__))

# 8 sec
_filename = os.path.join(_mydir, 'raw/yahoo/2010-01-01_to_2018-11-29')

try:
    df_orig
except NameError as e:
    df_orig = pd.read_parquet(_filename)

