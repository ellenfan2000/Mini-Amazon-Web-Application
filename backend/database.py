import sqlalchemy
import math
import struct
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.engine import URL
from sqlalchemy import Table, create_engine, MetaData, text, Column, Integer, String, Float, Sequence, ForeignKey, inspect
from sqlalchemy import Enum, Float, PrimaryKeyConstraint, DateTime, func
from sqlalchemy.orm import relationship, declarative_base, subqueryload

Base = declarative_base()

class User(Base):
    pass

class Products(Base):
    __tablename__ = "product"
    
    ID = Column(Integer, primary_key = True, autoincrement=True)
    

class Order(Base):
    __tablename__ = "order"

    orderID = Column(Integer, primary_key = True, autoincrement=True)
    pass

class Package(Base):
    __tablename__ = "package"

    packageID = Column(Integer, primary_key = True)
    pass

class Warehouse(Base):
    __tablename__ ="Warehouse"

    warehouseID = Column(Integer, primary_key = True, autoincrement=True)


    
def init():
    db_url = f"postgresql+psycopg2://postgres:passw0rd@db:5432/HW4"
    # db_url = f"postgresql+psycopg2://postgres:passw0rd@127.0.0.1:5432/HW4"
    engine = create_engine(db_url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine, checkfirst=True)

    return engine

def getEngine():
    db_url = f"postgresql+psycopg2://postgres:passw0rd@db:5432/HW4"
    # db_url = f"postgresql+psycopg2://postgres:passw0rd@127.0.0.1:5432/HW4"
    engine = create_engine(db_url)
    return engine
    
