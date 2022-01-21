from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
RDB_PATH = 'sqlite:///db.sqlite3'
ECHO_LOG = True

engine = create_engine(
    RDB_PATH, echo=ECHO_LOG, connect_args={'check_same_thread': False}
)

Session = sessionmaker(bind=engine)
session = Session()
