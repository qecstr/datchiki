from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql





URL_DATABASE = 'postgresql://postgres:esik2002@localhost:5432/datchiki'
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit = False,autoflush=False, bind=engine)
Base = declarative_base()
