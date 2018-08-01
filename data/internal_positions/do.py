import pandas as pd
import glob
from sqlalchemy import create_engine
import os
_mydir = os.path.realpath(os.path.dirname(__file__))
db = os.path.join(_mydir, 'db.sqlite3')
connection_string = 'sqlite:///{}'.format(db)
print(connection_string)
engine = create_engine(connection_string, echo=False)
filename = glob.glob('NON*.csv')
assert len(filename) == 1, 'got {}'.format(filename)
filename = filename[0]
df = pd.read_csv(filename)
df.to_sql('data', con=engine, index=False)
# d = engine.execute('select * from data').fetchall()
d = pd.read_sql('select * from data', engine)

