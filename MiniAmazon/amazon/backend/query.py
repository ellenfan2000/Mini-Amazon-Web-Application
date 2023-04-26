# import WorldMessage
# import UPSMessage
# try:
#     from .database import *
# except:
#     from database import *
from database import *

engine = getEngine()
Session = sessionmaker(bind=engine)
session = Session()
    
def get_recommend():
    global engine
    global session
    
    orders = session.query(Order.product_id, func.avg(Order.rate).label('avg_rate')).group_by(Order.product_id).order_by(func.avg(Order.rate).desc()).limit(5).subquery()
    re = session.query(Products.id, Products.name, orders.c.avg_rate).join(orders, orders.c.product_id == Products.id).order_by(orders.c.avg_rate.desc()).all()

    for p in re:
        print(p.id, p.name, p.avg_rate)
    session.commit()
    # session.close()
    return re

def get_search_res(user_input):
    # engine = getEngine()
    # Session = sessionmaker(bind=engine)
    # session = Session()
    global engine
    global session
    products = session.query(Products).filter(Products.name.ilike('%' +user_input + '%')).all()
    session.commit()
    # session.close()
    for p in products:
        print(p.id, p.name, p.category)
    return products


def get_product_detail(product_id):
    # engine = getEngine()
    # Session = sessionmaker(bind=engine)
    # session = Session()

    global engine
    global session

    re = session.query(Products).filter(Products.id == int(product_id)).first()
    comments = session.query(Order).join(Order.customer).filter(Order.product_id == int(product_id)).all()
    for i in comments:
        print(i.customer.username, i.id, i.rate, i.comment)
    session.commit()
    return re, comments 

def get_all_orders(user_id):
    # engine = getEngine()
    # Session = sessionmaker(bind=engine)
    # session = Session()

    global engine
    global session
    re = session.query(Order).join(Order.product).filter(Order.buyer == int(user_id)).all()
    for o in re:
        print(o.id, o.product.name, o.customer.username)
    session.commit()
    return re

def get_order_details(order_id):
    # engine = getEngine()
    # Session = sessionmaker(bind=engine)
    # session = Session()
    global engine
    global session

    # re = session.query(Order).join(Order.product).join(Order.package).filter(Order.id == int(order_id)).first()
    re = session.query(Order, Package).join(Order.product).join(Package, Order.package == Package.packageID).filter(Order.id == int(order_id)).first()
    
    print(re.id, re.product.name, re.customer.username, re.status)
    session.commit()
    return re
    # session.close()
