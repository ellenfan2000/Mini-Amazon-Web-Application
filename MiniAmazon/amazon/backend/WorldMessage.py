import world_amazon_pb2 as WORLD
from database import *

seqnum = 0
past_messages = {}

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
    global seqnum
    seqnum += 1
    pack.seqnum = seqnum
    for p in products:
        pack.things.append(p)
    
    global past_messages
    past_messages[seqnum] = pack
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
    global seqnum
    seqnum += 1
    purchase.seqnum = seqnum

    global past_messages
    past_messages[seqnum] = purchase
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

    # concurrent issue
    global seqnum
    seqnum += 1
    truck.seqnum = seqnum

    global past_messages
    past_messages[seqnum] = truck
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
    # concurrent issue
    global seqnum
    seqnum += 1
    query.seqnum = seqnum

    global past_messages
    past_messages[seqnum] = query
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
