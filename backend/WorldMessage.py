from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import socket
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import GPB.world_amazon_pb2 as WORLD
import socketUtils

seqnum = 0

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
    seqnum += 1
    pack.seqnum = seqnum
    for p in products:
        pack.things.append(p)
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
    seqnum += 1
    purchase.seqnum = seqnum
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
    seqnum += 1
    truck.seqnum = seqnum
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
    seqnum += 1
    query.seqnum = seqnum
    return query




def connect_to_World(world_socket,wordid,numwh):
    connect = WORLD.AConnect()
    # connect.worldid = wordid
    for i in range(numwh):
        wh = create_Awarehouse(i, i*10, i*10)
        connect.initwh.append(wh)
    connect.isAmazon = True
    response = WORLD.AConnected()
    while(True):
        socketUtils.send_message(world_socket, connect)
        response_str = socketUtils.recv_message(world_socket)
        response.ParseFromString(response_str)
        if(response.result == "connected!"):
            break
        else:
            print(response.result)



# if __name__ == '__main__':
#     world_socket = socket_connect("127.0.0.1", 23456)
#     connect_to_World(world_socket, 1, 3)