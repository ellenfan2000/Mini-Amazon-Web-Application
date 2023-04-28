
from database import *
import socketUtils
import struct


package_id = 0
def buy_product(user_id, product_id, amount, address):
    sock = socketUtils.socket_connect("vcm-30469.vm.duke.edu",29081)
    # modify databse，generate packageid,
    global package_id
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # need lock
    # package_id =session.execute(select(func.max(Order.id))).scalar()+1
    package_id += 1
    # 
    neworder = Order(buyer = user_id, product_id = product_id, amount = amount, status = 'packing', package = package_id)
    session.add(neworder)
    session.commit()
    product = session.query(Products).filter(Products.id == product_id).first()

    value = struct.pack('!I', package_id)
    sock.sendall(value)
    value = struct.pack('!I', address[0])
    sock.sendall(value)
    value = struct.pack('!I', address[1])
    sock.sendall(value)
    
    d = sock.recv(4)
    length = struct.unpack('!I', d)[0]
    message = sock.recv(length).decode()
    print(message)
    print(user_id,product_id,amount,address) 
    if(message == 'Success'):
        return neworder.id
    else:
        raise ValueError(message)

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

