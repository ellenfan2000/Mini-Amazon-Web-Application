import amazon_ups_pb2 as UPS
import world_amazon_pb2 as WORLD
import socketUtils
from database import *
from WorldMessage import WorldMessage
import copy
import time

import threading

class UPSMessage:
    lock_seq = threading.Lock()
    seqnum = 0
    ack_response = []

    def __init__(self):
        pass

    def get_seqnum(self):
        UPSMessage.lock_seq.acquire()
        UPSMessage.seqnum += 1
        UPSMessage.lock_seq.release()
        return UPSMessage.seqnum
    '''
    message Desti_loc{
        required int64 x = 1;
        required int64 y = 2;
    }
    '''
    def create_Desti(self, x, y):
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
    def create_RequestPickUp(self, pn, pkid, whid, x,y, uacc = None):
        pickup = UPS.ATURequestPickup()
        pickup.product_name = pn
        pickup.packageid = pkid
        if(uacc):
            pickup.ups_account = uacc
        pickup.whid = whid
        pickup.destination.x = x
        pickup.destination.y = y
        pickup.seqnum = self.get_seqnum()

        return pickup

    '''
    message ATULoaded{
        required int64 packageid = 1;
        required int64 truckid = 2;
        required int64 seqnum = 3;
    }
    '''
    def create_ATULoaded(self, truckid, pkids):
        loaded = UPS.ATULoaded()
        loaded.packageid.extend(pkids)
        loaded.truckid = truckid
        loaded.seqnum = self.get_seqnum()
        return loaded

    '''
    message AUErr{
        required string err = 1;
        required int64 originseqnum = 2;
        required int64 seqnum = 3;
    }
    '''
    def create_AUErr(self, err, ori_seqnum):
        auerr = UPS.AUErr()
        auerr.err = err
        auerr.originseqnum = ori_seqnum

        auerr.seqnum =self.get_seqnum()
        return auerr


    def handle_UTAArrived(self,engine, world_socket, ups_socket, message, world:WorldMessage):
        Session = sessionmaker(bind=engine)
        session = Session()
        packages_not_ready = [id for id in message.packageid]
        command = WORLD.ACommands()
        # waiting for all packages UPS need to be loaded 
        while(len(packages_not_ready) != 0):
            # print("Checking order status ...")
            need_send = False
            temp = copy.deepcopy(packages_not_ready)
            command = WORLD.ACommands()
            for id in temp:
                order = session.query(Order).filter(Order.package == id).with_for_update().first()
                # if packing, waiting for packed
                # if packed, send putOnTruck
                if order.status == 'packed':
                    need_send = True
                    command.load.append(world.create_APutOnTruck(message.whid, message.truckid, id))
                    order.status = 'loading'
                session.commit()
                # if loading, waiting for loaed
                #if loded, waiting for other package to be ready
                if order.status == 'loaded':
                    packages_not_ready.remove(id)
            if need_send:
                print('Send put on truck to World')
                socketUtils.send_message(world_socket, command)
            time.sleep(2)

        Ucommand = UPS.ATUCommands()
        Ucommand.loaded.append(WorldMessage.create_ATULoaded(message.truckid,message.packageid))
        print("Send loaded to UPS")
        socketUtils.send_message(ups_socket, Ucommand)
        session.close()
        pass

    def handle_UTAOutDelivery(self,session, message, command):
        order = session.query(Order).filter(Order.package == message.packageid).first()
        order.status = 'delivering'
        session.commit()

        command.acks.append(message.seqnum)
        UPSMessage.ack_response.append(message.seqnum)
        pass


    def handle_Delivery(self,session, message, command):
        order = session.query(Order).filter(Order.package == message.packageid).first()
        order.status = 'delivered'
        session.commit()

        command.acks.append(message.seqnum)
        UPSMessage.ack_response.append(message.seqnum)
        pass
