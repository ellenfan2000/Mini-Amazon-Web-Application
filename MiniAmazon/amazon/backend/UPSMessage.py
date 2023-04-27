import amazon_ups_pb2 as UPS
import world_amazon_pb2 as WORLD
import socketUtils
from database import *
import WorldMessage
import copy
import time

import threading

ups_lock_seq = threading.Lock()
UPS_seqnum = 0

def get_seqnum():
    global UPS_seqnum
    ups_lock_seq.acquire()
    UPS_seqnum += 1
    ups_lock_seq.release()
    return UPS_seqnum
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
    return dest

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
def create_RequestPickUp(pn, pkid, whid, x,y, uacc = None):
    pickup = UPS.ATURequestPickup()
    pickup.product_name = pn
    pickup.packageid = pkid
    if(uacc):
        pickup.ups_account = uacc
    pickup.whid = whid
    pickup.destination.x = x
    pickup.destination.y = y
    pickup.seqnum = get_seqnum()

    return pickup

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
    loaded.seqnum = get_seqnum()
    return loaded

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

    auerr.seqnum = get_seqnum()
    return auerr

def handle_UTAArrived(world_socket, ups_socklet, session, message):
    packages_not_ready = [id for id in message.packageid]
    # waiting for all packages UPS need to be loaded 
    while(len(packages_not_ready) != 0):
        need_send = False
        temp = copy.deepcopy(packages_not_ready)
        command = WORLD.ACommands()
        for id in temp:
            order = session.query(Order).filter(Order.package == id).first()
            # if packed, then ask World to Load
            if order.status == 'packed':
                command.load.append(WorldMessage.create_APutOnTruck(message.whid, message.truckid, id))
                need_send = True
            #if loded, waiting for other package to be ready
            if order.status == 'loaded':
                packages_not_ready.remove(id)
        if need_send:
            print('Send put on truck')
            socketUtils.send_message(world_socket, command)
        time.sleep(1)

    ULoaded = create_ATULoaded(message.packageid,message.truckid)
    print("Send loaded")
    socketUtils.send_message(ups_socklet, ULoaded)
    pass


def handle_UTAOutDelivery(session, message):
    order = session.query(Order).filter(Order.package == message.packageid).first()
    order.status = 'delivering'
    session.commit()
    pass


def handle_Delivery(session, message):
    order = session.query(Order).filter(Order.package == message.packageid).first()
    order.status = 'delivered'
    session.commit()
    pass
