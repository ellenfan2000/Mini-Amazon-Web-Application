import sqlalchemy
import math
import struct
from sqlalchemy.orm import sessionmaker, mapper
from datetime import datetime
from sqlalchemy.engine import URL
from sqlalchemy import Table, create_engine, MetaData, text, inspect
from sqlalchemy import Column, Integer, Text, Float, ForeignKey, String, CheckConstraint
from sqlalchemy import Enum, Float, PrimaryKeyConstraint, DateTime, func
from sqlalchemy.orm import relationship, declarative_base, subqueryload

Base = declarative_base()

class User(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    password = Column(String(128))
    email = Column(String(254), unique=True)
    first_name = Column(String(30))
    last_name = Column(String(150))
    is_staff = Column(Integer)
    is_active = Column(Integer)
    date_joined = Column(String(40))

class Warehouse(Base):
    __tablename__ ="warehouse"

    id = Column(Integer, primary_key = True, autoincrement=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)


class Products(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key = True, autoincrement=True)
    description = Column(Text)
    price = Column(Float)
    inventory = Column(Integer)
    warehouse = Column(Integer, ForeignKey('warehouse.id'))
    
class Package(Base):
    __tablename__ = "package"

    id = Column(Integer, primary_key = True, autoincrement=True)
    packageID = Column(Integer, unique=True)
    warehouse = Column(Integer, ForeignKey('warehouse.id'))
    address_x = Column(Integer, nullable=False)
    address_y = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key = True, autoincrement=True)
    buyer = Column(Integer, ForeignKey('auth_user.id'))
    product = Column(Integer, ForeignKey('product.id'))
    status = Column(String, CheckConstraint("status IN ('packing', 'packed', 'loading', 'loaded', 'delivering', 'delivered')"))
    package = Column(Integer, ForeignKey('package.id'))

def init():
    # db_url = f"postgresql+psycopg2://postgres:passw0rd@db:5432/Amazon"
    db_url = f"postgresql+psycopg2://postgres:passw0rd@127.0.0.1:5432/Amazon"
    engine = create_engine(db_url)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine, checkfirst=True)
    
    return engine

def getEngine():
    # db_url = f"postgresql+psycopg2://postgres:passw0rd@db:5432/Amazon"
    db_url = f"postgresql+psycopg2://postgres:passw0rd@127.0.0.1:5432/Amazon"
    engine = create_engine(db_url)
    return engine
    
