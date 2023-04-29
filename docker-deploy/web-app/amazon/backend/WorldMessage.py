import world_amazon_pb2 as WORLD
from database import *
import threading
import socketUtils

class WorldMessage:
    lock_seq = threading.Lock()
    lock_resend = threading.Lock()

    seqnum = 0
    past_messages = {}
    ack_response = []

    def __init__(self):
        pass

    def get_seqnum(self):
        WorldMessage.lock_seq.acquire()
        WorldMessage.seqnum += 1
        WorldMessage.lock_seq.release()
        return WorldMessage.seqnum



    def add_message(self, message):
        if(message.seqnum not in WorldMessage.past_messages.keys()):
            WorldMessage.lock_resend.acquire()
            WorldMessage.past_messages[message.seqnum] = message
            WorldMessage.lock_resend.release()



    def create_Awarehouse(self, id,x,y):
        wh = WORLD.AInitWarehouse()
        wh.id = id
        wh.x = x
        wh.y = y
        return wh

    def create_Aproduct(self, id, desc, count):
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
    def create_APack(self, whnum, shipid, *products):
        pack = WORLD.APack()
        pack.whnum = whnum
        pack.shipid = shipid

        # concurrent issue
        pack.seqnum = self.get_seqnum()
        pack.things.extend(products)
        
        self.add_message(pack)
        
        return pack


    '''
    message APurchaseMore{
    required int32 whnum = 1;
    repeated AProduct things = 2;
    required int64 seqnum = 3;
    }
    '''
    def create_APurchaseMore(self, whnum, *products):
        purchase = WORLD.APurchaseMore()
        purchase.whnum = whnum
        purchase.things.extend(products)
    
        purchase.seqnum = self.get_seqnum()
        self.add_message(purchase)
        return purchase


    '''
    message APutOnTruck{
    required int32 whnum = 1;
    required int32 truckid = 2;
    required int64 shipid = 3;
    required int64 seqnum = 4;
    }
    '''
    def create_APutOnTruck(self, whnum, truckid, shipid):
        truck = WORLD.APutOnTruck()
        truck.whnum = whnum
        truck.truckid = truckid
        truck.shipid = shipid

        truck.seqnum = self.get_seqnum()
        self.add_message(truck)
        return truck

    '''
    message AQuery{
    required int64 packageid = 1;
    required int64 seqnum = 2;
    }
    '''
    def create_AQuery(self, pkid):
        query = WORLD.AQuery()
        query.packageid = pkid
        query.seqnum = self.get_seqnum()
        self.add_message(query)
        return query


    def send_ack(self, world_socket, mseqnum):
        command = WORLD.ACommands()
        command.acks.append(mseqnum)
        WorldMessage.ack_response.append(mseqnum)
        socketUtils.send_message(world_socket, command)


    '''
    when receive ApurchaseMore message from world, add product inventory
    '''
    def handle_APurchaseMore(self, session, message, world_socket):
        if(message.seqnum in WorldMessage.ack_response):
            return
        self.send_ack(world_socket, message.seqnum)
        for p in message.things:
            product = session.query(Products).filter(Products.id == p.id).filter(Products.name == p.description).with_for_update().first()
            product.inventory += p.count
            session.commit()
        pass


    '''
    when receive APacked message from world, update product status
    '''
    def handle_APacked(self, session, message, world_socket):
        if(message.seqnum in WorldMessage.ack_response):
            return
        self.send_ack(world_socket, message.seqnum)
        order = session.query(Order).filter(Order.package ==  message.shipid).with_for_update().first()
        order.status = 'packed'
        session.commit()


    def handle_ALoaded(self, session, message, world_socket):
        if(message.seqnum in WorldMessage.ack_response):
            return
        self.send_ack(world_socket, message.seqnum)
        order = session.query(Order).filter(Order.package ==  message.shipid).with_for_update().first()
        order.status = 'loaded'
        session.commit()


    def handle_APackage(self, session, message, world_socket):
        if(message.seqnum in WorldMessage.ack_response):
            return
        self.send_ack(world_socket, message.seqnum)
        order = session.query(Order).filter(Order.package ==  message.packageid).with_for_update().first()
        order.status = message.status
        session.commit()

    def handle_error(self, session, message, world_socket):
        if(message.seqnum in WorldMessage.ack_response):
            return
        self.send_ack(world_socket, message.seqnum)
        print(message.err)
        print(message.originseqnum, WorldMessage.past_messages)
        WorldMessage.lock_resend.acquire()
        if(message.originseqnum in WorldMessage.past_messages):
            past = WorldMessage.past_messages.pop(message.originseqnum)
            if(past.DESCRIPTOR.name == 'APack' or past.DESCRIPTOR.name == 'APutOnTruck'):
                order = session.query(Order).filter(Order.package == past.shipid).with_for_update().first()
                order.status = 'canceled'
                session.commit()
        WorldMessage.lock_resend.release()

    def resend(self):
        need_resend = False
        WorldMessage.lock_resend.acquire()
        past_messages = WorldMessage.past_messages
        command = WORLD.ACommands()
        for m in past_messages.values():
            if (m.DESCRIPTOR.name == 'APurchaseMore'):
                need_resend = True
                command.buy.append(m)
            elif (m.DESCRIPTOR.name == 'APack'):
                need_resend = True
                command.topack.append(m)
            elif (m.DESCRIPTOR.name == 'APutOnTruck'):
                need_resend = True
                command.load.append(m)
            elif (m.DESCRIPTOR.name == 'AQuery'):
                need_resend = True
                command.queries.append(m)
        WorldMessage.lock_resend.release()
        if(need_resend):
            print("Resending...")
            print(past_messages.keys())
            return command
        return None

