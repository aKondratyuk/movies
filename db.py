BASE = 'postgresql+psycopg2'
USERNAME = 'kinoua'
PASSWORD = '1234'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'kino'

secret = "secret"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = '{base}://{user}:{pw}@{host}:{port}/{db}'.format(base=BASE, user=USERNAME, pw=PASSWORD, host=HOST, port=PORT, db=DATABASE)

engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()

metadata = Base.metadata
