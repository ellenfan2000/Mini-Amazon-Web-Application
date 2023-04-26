from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import socket
import world_amazon_pb2 as WORLD
import socketUtils
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
when receive ApurchaseMore message from world
'''
def handle_APurchaseMore(session, message):
    for p in message.things:
        product = session.query(Products).filter(Products.id == p.id).filter(Products.name == p.description).with_for_update().first()
        product.inventory += p.count
        session.commit()
    pass

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



def connect_to_World(world_socket,wordid,warehouses):
    connect = WORLD.AConnect()
    # connect.worldid = wordid
    for w in warehouses:
        print(w.id, w.x, w.y)
        wh = create_Awarehouse(w.id, w.x, w.y)
        connect.initwh.append(wh)
    connect.isAmazon = True
    response = WORLD.AConnected()
    while(True):
        socketUtils.send_message(world_socket, connect)
        response_str = socketUtils.recv_message(world_socket)
        response.ParseFromString(response_str)
        print(response.result)
        if(response.result == "connected!"):
            break
        else:
            print(response.result)


def init_world(world_socket, session, products):
    command = WORLD.ACommands()
    for p in products:
        command.buy.append(create_APurchaseMore(p.warehouse_id, create_Aproduct(p.id, p.name, p.inventory)))
    command.disconnect = False

    while True:
        socketUtils.send_message(world_socket, command)
        print(command.DESCRIPTOR.name)
        for c in command.buy:
            print(c.seqnum)

        try:
            world_reponse = WORLD.AResponses()
            world_reponse.ParseFromString(socketUtils.recv_message(world_socket))
            # if(world_reponse.HasField('arrived')):
            for i in world_reponse.arrived:
                print("Seqnums are " + str(i.seqnum))

            for i in world_reponse.acks:
                print("Acks are : " + str(i))
            for i in world_reponse.error:
                print(i.err)
            return
        except Exception as e:
            print(e)

def resend_message(world_socket):
    global past_messages
    command = WORLD.ACommands()
    for m in past_messages.items:
        if(m.DESCRIPTOR.name == 'APurchaseMore'):
            command.buy.append(m)
        elif(m.DESCRIPTOR.name == 'APack'):
            command.topack.append(m)
        elif(m.DESCRIPTOR.name == 'APutOnTruck'):
            command.load.append(m)
        elif(m.DESCRIPTOR.name == 'AQuery'):
            command.queries.append(m)
    socketUtils.send_message(world_socket, command)



# if __name__ == '__main__':
#     world_socket = socket_connect("127.0.0.1", 23456)
#     connect_to_World(world_socket, 1, 3)