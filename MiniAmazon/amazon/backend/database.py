# import sqlalchemy
# import math
# import struct
from sqlalchemy.orm import sessionmaker, mapper
from datetime import datetime
from sqlalchemy.engine import URL
from sqlalchemy import Table, create_engine, MetaData, text, inspect,select
from sqlalchemy import Column, Integer, Text, Float, ForeignKey, String, CheckConstraint, LargeBinary
from sqlalchemy import Enum, Float, PrimaryKeyConstraint, DateTime, func
from sqlalchemy.orm import relationship, declarative_base, subqueryload

Base = declarative_base()

class AuthUser(Base):
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
    name = Column(Text, nullable=False)
    description = Column(Text, nullable = True)
    # picture = Column(LargeBinary)
    price = Column(Float)
    category = Column(Text, nullable = True)
    inventory = Column(Integer)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'))
    warehouse = relationship('Warehouse', backref="product_warehouse_id")
    
class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key = True, autoincrement=True)
    buyer = Column(Integer, ForeignKey('auth_user.id'))
    customer = relationship('AuthUser')
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Products', backref="order_product_id")
    amount = Column(Integer)
    status = Column(String, CheckConstraint("status IN ('packing', 'packed', 'loading', 'loaded', 'delivering', 'delivered')"))
    package = Column(Integer, unique=True)
    rate = Column(Float, nullable=True)
    comment = Column(Text)
    
class Package(Base):
    __tablename__ = "package"

    id = Column(Integer, primary_key = True, autoincrement=True)
    packageID = Column(Integer, ForeignKey('order.package') )
    order = relationship('Order')
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'))
    warehouse = relationship('Warehouse')
    address_x = Column(Integer, nullable=False)
    address_y = Column(Integer, nullable=False)

def initDataBase():
    # db_url = f"postgresql+psycopg2://postgres:passw0rd@db:5432/Amazon"
    # db_url = f"postgresql+psycopg2://postgres:passw0rd@127.0.0.1:5432/Amazon"
    engine = create_engine("postgresql+psycopg2://postgres:passw0rd@127.0.0.1:5432/Amazon")
    Base.metadata.drop_all(engine, [Warehouse.__table__, Products.__table__, Package.__table__, Order.__table__])
    Base.metadata.create_all(engine, checkfirst=True)
    
    return engine

def getEngine():
    # db_url = f"postgresql+psycopg2://postgres:passw0rd@db:5432/Amazon"
    db_url = "postgresql+psycopg2://postgres:passw0rd@127.0.0.1:5432/Amazon"
    engine = create_engine(db_url)

    return engine
    
