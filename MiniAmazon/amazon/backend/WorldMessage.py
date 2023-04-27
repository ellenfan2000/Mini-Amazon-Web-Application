import world_amazon_pb2 as WORLD
from database import *
import threading

lock_seq = threading.Lock()
lock_resend = threading.Lock()

seqnum = 0
past_messages = {}

def get_seqnum():
    global seqnum
    lock_seq.acquire()
    seqnum += 1
    lock_seq.release()
    return seqnum



def add_message(message):
    global past_messages
    lock_resend.acquire()
    past_messages[seqnum] = message
    lock_resend.release()



def create_Awarehouse(id,x,y):
    wh = WORLD.AInitWarehouse()
    wh.id = id
    wh.x = x
    wh.y = y
    return wh

def create_Aproduct(id, desc, count):
    product = WORLD.AProduct()
    product.id = id
    product.description = desc
    product.count = count
    return product

'''
message APack{
  required int32 whnum = 1;
  repeated AProduct things = 2;
  required int64 shipid = 3;
  required int64 seqnum = 4;
}
'''
def create_APack(whnum, shipid, *products):
    pack = WORLD.APack()
    pack.whnum = whnum
    pack.shipid = shipid

    # concurrent issue
    pack.seqnum = get_seqnum()
    for p in products:
        pack.things.append(p)
    
    add_message(pack)
    
    return pack


'''
message APurchaseMore{
  required int32 whnum = 1;
  repeated AProduct things = 2;
  required int64 seqnum = 3;
}
'''
def create_APurchaseMore(whnum, *products):
    purchase = WORLD.APurchaseMore()
    purchase.whnum = whnum
    for p in products:
        purchase.things.append(p)
    # concurrent issue
    purchase.seqnum = get_seqnum()
    add_message(purchase)
    return purchase


'''
message APutOnTruck{
  required int32 whnum = 1;
  required int32 truckid = 2;
  required int64 shipid = 3;
  required int64 seqnum = 4;
}
'''
def create_APutOnTruck(whnum, truckid, shipid):
    truck = WORLD.APutOnTruck()
    truck.whnum = whnum
    truck.truckid = truckid
    truck.shipid = shipid

    truck.seqnum = get_seqnum()
    add_message(truck)
    return truck

'''
message AQuery{
  required int64 packageid = 1;
  required int64 seqnum = 2;
}
'''
def create_AQuery(pkid):
    query = WORLD.AQuery()
    query.packageid = pkid
    query.seqnum = get_seqnum()
    add_message(query)
    return query


'''
when receive ApurchaseMore message from world, add product inventory
'''
def handle_APurchaseMore(session, message):
    for p in message.things:
        product = session.query(Products).filter(Products.id == p.id).filter(Products.name == p.description).with_for_update().first()
        product.inventory += p.count
        session.commit()
    pass


'''
when receive APacked message from world, update product status
'''
def handle_APacked(session, message):
    order = session.query(Order).filter(Order.package ==  message.shipid).with_for_update().first()
    order.status = 'packed'
    session.commit()


def handle_ALoaded(session, message):
    order = session.query(Order).filter(Order.package ==  message.shipid).with_for_update().first()
    order.status = 'loaded'
    session.commit()


def handle_APackage(session, message):
    order = session.query(Order).filter(Order.package ==  message.packageid).with_for_update().first()
    order.status = message.status
    session.commit()
