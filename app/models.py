from app.database import Base
from sqlalchemy import types
from sqlalchemy import Column,Integer






class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True,index=True)
    login = Column(types.TEXT,index=True)
    password = Column(types.TEXT, index=True)


class Data(Base):
    __tablename__ = 'Data'
    id = Column(Integer,primary_key=True,index= True)
    time = Column(types.TIME,index=True)
    temperature = Column(types.FLOAT,index= True)
    humidity = Column(types.FLOAT,index=True)
    CO2 = Column(types.FLOAT,index = True)