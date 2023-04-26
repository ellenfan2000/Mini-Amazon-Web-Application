from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import socket
import os
import sys
import amazon_ups_pb2 as UPS
import socketUtils

seqnum = 0

'''
message Desti_loc{
    required int64 x = 1;
    required int64 y = 2;
}
'''
def create_Desti(x, y):
    dest = UPS.Desti_loc()
    dest.x = x
    dest.y = y
    pass

'''
message ATURequestPickup{
    required string product_name = 1;
    required int64 packageid = 2;
    optional string ups_account = 3;
    required int64 whid = 4;
    required Desti_loc destination = 5;
    required int64 seqnum = 6;
}
'''
def create_RequestPickUp(pn, pkid, whid, dest, uacc = None):
    pickup = UPS.ATURequestPickup()
    pickup.product_name = pn
    pickup.packageid = pkid
    if(uacc):
        pickup.ups_account = uacc
    pickup.whid = whid
    pickup.destination = dest

    # need concurrent
    seqnum += 1
    pickup.seqnum = seqnum
    pass

'''
message ATULoaded{
    required int64 packageid = 1;
    required int64 truckid = 2;
    required int64 seqnum = 3;
}
'''
def create_ATULoaded(pkid, truckid):
    loaded = UPS.ATULoaded()
    loaded.packageid = pkid
    loaded.truckid = truckid

    # need concurrent
    seqnum += 1
    loaded.seqnum = seqnum
    pass

'''
message AUErr{
    required string err = 1;
    required int64 originseqnum = 2;
    required int64 seqnum = 3;
}
'''
def create_AUErr(err, ori_seqnum):
    auerr = UPS.AUErr()
    auerr.err = err
    auerr.originseqnum = ori_seqnum

    # need concurrent
    seqnum += 1
    auerr.seqnum = seqnum
    pass

def connect_to_UPS(ups_socket, world_id):
    auc = UPS.AUConnected()
    auc.worldid = world_id
    socketUtils.send_message(ups_socket, auc)
    

def handle_UTAArrived():
    pass

def handle_UTAOutDelivery():
    pass

def handle_Delivery():
    pass
