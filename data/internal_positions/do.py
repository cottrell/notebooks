import pandas as pd
import glob
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
filename = glob.glob('NON*.csv')
assert len(filename) == 1, 'got {}'.format(filename)
filename = filename[0]
df = pd.read_csv(filename)
df.to_sql('data', con=engine, index=False)
# d = engine.execute('select * from data').fetchall()
d = pd.read_sql('select * from data', engine)

