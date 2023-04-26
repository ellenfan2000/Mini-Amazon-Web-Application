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
        print(p.id, p.name)
    return products


def get_product_detail(product_id):
    # engine = getEngine()
    # Session = sessionmaker(bind=engine)
    # session = Session()

    global engine
    global session

    re = session.query(Products).filter(Products.id == int(product_id)).first()
    print(re.id, re.name)

    session.commit()
    return re

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

    re = session.query(Order).join(Order.product).filter(Order.id == int(order_id)).first()
    print(o.id, o.product.name, o.customer.username)
    session.commit()
    # session.close()


# for test
# if __name__ == '__main__':
#     engine = initDataBase()
#     warehouses = [Warehouse(id = 0, x = 1, y = 1),
#                   Warehouse(id = 1, x = 2, y = 2),
#                   Warehouse(id = 2, x = 3, y = 3)]

#     products =[Products(id = 0, name = "Kindle Paperwhite (8 GB)", price =139.99, category = "Digital", inventory = 500, warehouse_id= 0),
#                Products(id = 1, name = "LG 34\" LED Monitor", price = 319.99, category = "Digital", inventory = 200, warehouse_id= 0),
#                Products(id = 2, name = "WUZHOU Tulip Plush Toy", price = 16.59, category ="Toy", inventory = 269, warehouse_id= 1),
#                Products(id = 3, name = "Jellycat Amuseables Cloud Plush", price = 39.99, category = "Top", inventory = 340, warehouse_id= 1),
#                Products(id = 4, name = "Women's Open Front Knit Coat", price = 69.99, category = "Cloth", inventory = 189, warehouse_id= 2),
#                Products(id = 5, name = "Men's Notch Lapel Double Trench Coat", price = 79.99, category = "Cloth", inventory = 230, warehouse_id= 2)
#                ]
    
#     orders = [Order(buyer = 2, product_id = 0, amount = 1, status = 'packed', package = 1, rate = 1), 
#               Order(buyer = 2, product_id = 1, amount = 1, status = 'packed', package = 2, rate = 3), 
#               Order(buyer = 2, product_id = 2, amount = 1, status = 'packed', package = 3, rate = None), 
#               Order(buyer = 2, product_id = 3, amount = 1, status = 'packed', package = 4, rate = 5), 
#               Order(buyer = 1, product_id = 4, amount = 1, status = 'packed', package = 5, rate = 2), 
#               Order(buyer = 1, product_id = 5, amount = 1, status = 'packed', package = 6, rate = 6), 
#               Order(buyer = 1, product_id = 0, amount = 1, status = 'packed', package = 7, rate = 8), 
#               Order(buyer = 1, product_id = 1, amount = 1, status = 'packed', package = 8, rate = 1), 
#               Order(buyer = 1, product_id = 2, amount = 1, status = 'packed', package = 9, rate = 0), 
#               ]
    
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     for wh in warehouses:
#         session.add(wh)
#     session.commit()
#     for p in products:
#         session.add(p)
#     session.commit()
#     for o in orders:
#         session.add(o)
#     session.commit()
#     get_recommend()
#     get_search_res('plush')
#     get_product_detail(5)
#     get_all_orders(2)
#     get_order_details(1)