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
    lock_resend = threading.Lock()
    seqnum = 0
    ack_response = []
    past_messages = {}

    def __init__(self):
        pass

    def get_seqnum(self):
        UPSMessage.lock_seq.acquire()
        UPSMessage.seqnum += 1
        UPSMessage.lock_seq.release()
        return UPSMessage.seqnum

    def add_message(self, message):
        if(message.seqnum not in UPSMessage.past_messages.keys()):
            UPSMessage.lock_resend.acquire()
            UPSMessage.past_messages[message.seqnum] = message
            UPSMessage.lock_resend.release()
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
        self.add_message(pickup)
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
        self.add_message(loaded)
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
        self.add_message(auerr)
        return auerr


    def handle_UTAArrived(self,engine, world_socket, ups_socket, message, world:WorldMessage):
        command = UPS.ATUCommands()
        command.acks.append(message.seqnum)
        socketUtils.send_message(ups_socket, command)
        Session = sessionmaker(bind=engine)
        session = Session()
        packages_not_ready = [id for id in message.packageid]
        command = WORLD.ACommands()
        # waiting for all packages UPS need to be loaded 
        while(len(packages_not_ready) != 0):
            break_i = False
            print("Checking order status ... ")
            print(packages_not_ready)
            need_send = False
            temp = copy.deepcopy(packages_not_ready)
            command = WORLD.ACommands()
            for id in temp:
                order = session.query(Order).filter(Order.package == id).with_for_update().first()
                print(order.status)
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
                    print(1, id)
                    packages_not_ready.remove(id)
                    print(packages_not_ready)
                    print(len(packages_not_ready))
                    if(len(packages_not_ready) == 0):
                        break_i = True
                        break
            
            if(break_i):
                break
            if need_send:
                print('Send put on truck to World')
                socketUtils.send_message(world_socket, command)
            time.sleep(3)

        Ucommand = UPS.ATUCommands()
        Ucommand.loaded.append(self.create_ATULoaded(message.truckid,message.packageid))
        print("Send loaded to UPS")
        socketUtils.send_message(ups_socket, Ucommand)
        session.close()
        pass

    def handle_UTAOutDelivery(self,session, message,ups_socket, command):
        command = UPS.ATUCommands()
        command.acks.append(message.seqnum)
        socketUtils.send_message(ups_socket, command)
        order = session.query(Order).filter(Order.package == message.packageid).first()
        order.status = 'delivering'
        session.commit()

        command.acks.append(message.seqnum)
        UPSMessage.ack_response.append(message.seqnum)
        pass


    def handle_Delivery(self,session, message, ups_socket,command):
        command = UPS.ATUCommands()
        command.acks.append(message.seqnum)
        socketUtils.send_message(ups_socket, command)

        order = session.query(Order).filter(Order.package == message.packageid).first()
        order.status = 'delivered'
        session.commit()

        command.acks.append(message.seqnum)
        UPSMessage.ack_response.append(message.seqnum)
        pass


    def resend(self):
        need_resend = False
        UPSMessage.lock_resend.acquire()
        past_messages = UPSMessage.past_messages

        command = UPS.ATUCommands()
        for m in past_messages.values():
            if (m.DESCRIPTOR.name == 'ATURequestPickup'):
                need_resend = True
                command.topickup.append(m)
            elif (m.DESCRIPTOR.name == 'ATULoaded'):
                need_resend = True
                command.loaded.append(m)
        UPSMessage.lock_resend.release()
        if(need_resend):
            print("Resending...")
            return command
        return None
