# pip install MySQL-python - no py3
# pip install cymysql
# pip install mysqlclient
# pip install psycopg2
import pandas as pd
import glob
from sqlalchemy import create_engine
import os
_mydir = os.path.realpath(os.path.dirname(__file__))
# db = os.path.join(_mydir, 'db.sqlite3')
# connection_string = 'sqlite:///{}'.format(db)
# connection_string = 'mysql+cymysql://localhost:3306/foo'
def create_db(name='test'):
    connection_string = 'postgresql+psycopg2://localhost/postgres'
    engine = create_engine(connection_string, echo=True)
    conn = engine.connect()
    conn.execute('commit')
    res = pd.read_sql('SELECT * FROM pg_database', conn)
    if name in res.values:
        print('{} exists'.format(name))
    else:
        conn.execute('create database {}'.format(name))
    conn.close()

dbname = 'test'
create_db(name=dbname)
connection_string = 'postgresql+psycopg2://localhost/{}'.format(dbname)
print(connection_string)
engine = create_engine(connection_string, echo=False)
conn = engine.connect()

filename = glob.glob('NON*.csv')
assert len(filename) == 1, 'got {}'.format(filename)
filename = filename[0]
df = pd.read_csv(filename)
df.to_sql('data', con=engine, index=False, if_exists='replace')
# d = engine.execute('select * from data').fetchall()
d = pd.read_sql('select * from data', engine)
