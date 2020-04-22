#!/usr/bin/env python
import pandas as pd

import sys

df = pd.read_csv(sys.argv[1])
if 'date' in df.columns:
    df = df.set_index('date')
    df = df.sort_index(ascending=False)
df.to_markdown(sys.stdout)
