import world_amazon_pb2 as WORLD
from database import *
import threading

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
        # for p in products:
        #     pack.things.append(p)
        
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
        # for p in products:
        #     purchase.things.append(p)
        # concurrent issue
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


    '''
    when receive ApurchaseMore message from world, add product inventory
    '''
    def handle_APurchaseMore(self, session, message, command):
        for p in message.things:
            product = session.query(Products).filter(Products.id == p.id).filter(Products.name == p.description).with_for_update().first()
            product.inventory += p.count
            session.commit()
        pass


    '''
    when receive APacked message from world, update product status
    '''
    def handle_APacked(self, session, message, command):
        order = session.query(Order).filter(Order.package ==  message.shipid).with_for_update().first()
        order.status = 'packed'
        session.commit()

        command.acks.append(message.seqnum)
        WorldMessage.ack_response.append(message.seqnum)


    def handle_ALoaded(self, session, message, command):
        order = session.query(Order).filter(Order.package ==  message.shipid).with_for_update().first()
        order.status = 'loaded'
        session.commit()

        command.acks.append(message.seqnum)
        WorldMessage.ack_response.append(message.seqnum)


    def handle_APackage(self, session, message, command):
        order = session.query(Order).filter(Order.package ==  message.packageid).with_for_update().first()
        order.status = message.status
        session.commit()

        command.acks.append(message.seqnum)
        WorldMessage.ack_response.append(message.seqnum)

    def handle_error(self, session, message):
        origin
