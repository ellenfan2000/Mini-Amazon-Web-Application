
from database import *
from WorldMessage import *
from UPSMessage import *
import amazon_ups_pb2 as UPS



package_id = 0
def buy_product(user_id, product_id, amount, address):

    # modify databse，generate packageid,
    global package_id
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # need lock
    package_id =session.execute(select(func.max(Order.id))).scalar()+1
    # 
    neworder = Order(buyer = user_id, product_id = product_id, amount = amount, status = 'packing', package = package_id)
    product = session.query(Products).filter(Products.id == product_id).first()

    # send ATURequestPickUp, 
    Umessage = create_RequestPickUp(product.name, package_id, product.warehouse_id, create_Desti(address[0], address[1]))
    Ucommand = UPS.ATUCommands()
    Ucommand.topickup.append(Umessage)


    # send Apacking
    Wmessage = create_APack(product.warehouse_id,package_id,create_Aproduct(product.id,product.name, amount))
    Wcommand = WORLD.ACommands()
    Wcommand.apack.append(Wmessage)

    newpackage = Package(packageID = package_id, warehouse_id = product.warehouse_id, address_x = address[0],address_y =address[1])
    session.add(neworder)
    session.commit()
    session.add(newpackage)
    session.commit()
    print(user_id,product_id,amount,address)
    # modify databse，generate packageid, send ATURequestPickUp, 
    pass

def set_comments(user_id, order_id, rate, content):
   
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    session = Session()

    order = session.query(Order).filter(Order.id == order_id).filter(Order.buyer == user_id).with_for_update().first()
    if(rate):
        order.rate = rate

    if(content):
        order.comment = content

    session.commit()
    session.close()
    print(user_id,order_id,rate,content)

