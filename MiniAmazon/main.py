import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# from backend.database import *
from amazon.backend.database import *
from amazon.backend import socketUtils, UPSMessage, WorldMessage, request, query
from amazon.backend import amazon_ups_pb2 as UPS
from amazon.backend import world_amazon_pb2 as WORLD
import socket

def initServer(engine, ups_socket, world_socket):
    Session = sessionmaker(bind=engine)
    session = Session()
    warehouses = [Warehouse(id = 0, x = 1, y = 1),
                  Warehouse(id = 1, x = 2, y = 2),
                  Warehouse(id = 2, x = 3, y = 3)]
    
    products =[Products(id = 0, name = "Kindle Paperwhite (8 GB)", price =139.99, category = "Digital", inventory = 500, warehouse_id= 0),
               Products(id = 1, name = "LG 34\" LED Monitor", price = 319.99, category = "Digital", inventory = 200, warehouse_id= 0),
               Products(id = 2, name = "WUZHOU Tulip Plush Toy", price = 16.59, category ="Toy", inventory = 269, warehouse_id= 1),
               Products(id = 3, name = "Jellycat Amuseables Cloud Plush", price = 39.99, category = "Top", inventory = 340, warehouse_id= 1),
               Products(id = 4, name = "Women's Open Front Knit Coat", price = 69.99, category = "Cloth", inventory = 189, warehouse_id= 2),
               Products(id = 5, name = "Men's Notch Lapel Double Trench Coat", price = 79.99, category = "Cloth", inventory = 230, warehouse_id= 2)
               ]
    
    # uconnect= UPS.UTAConnect()
    # uconnect.ParseFromString(socketUtils.recv_message(ups_socket))

    WorldMessage.connect_to_World(world_socket,1,warehouses)
      # WorldMessage.connect_to_World(world_socket,uconnect.worldid,warehouses)
    for wh in warehouses:
        session.add(wh)
    session.commit()

    WorldMessage.init_world(world_socket, products)
    # for p in products:
    #     session.add(p)
    session.commit()
    # UPSMessage.connect_to_UPS(ups_socket, uconnect.worldid)



def handle_world_response(world_socket, session):
    while True:
        command = WORLD.ACommands()
        world_reponse = WORLD.AResponses()
        world_reponse.ParseFromString(socketUtils.recv_message(world_socket))

        
        for i in world_reponse.acks:
            if(i in WorldMessage.past_messages):
                WorldMessage.past_messages.pop(i)

        for m in world_reponse.arrived:
            WorldMessage.handle_APurchaseMore(session,m)
            command.acks.append(m.seqnum)
        for m in world_reponse.ready:
            WorldMessage.handle_APacked(session,m)
            command.acks.append(m.seqnum)
        for m in world_reponse.loaded:
            WorldMessage.handle_ALoaded(session,m)
            command.acks.append(m.seqnum)
        for m in world_reponse.packagestatus:
            WorldMessage.handle_APackage(session,m)
            command.acks.append(m.seqnum)
        socketUtils.send_message(world_socket, command)
        
        for i in world_reponse.error:
            print(i.err)
        pass


def handle_ups_response(ups_socket, session):
    pass

def handle_resend(world_socket, ups_socket):
    WorldMessage.resend_message()
    pass
'''
    protoc -I=./ --python_out=./ amazon_ups.proto
'''
if __name__ == '__main__':
    engine = initDataBase()
    # engine = getEngine()
    print("database initialized")
    # ups_hostname = "0.0.0.0"
    # ups_socket = socketUtils.socket_connect(ups_hostname, 32345)

    world_hostname = "0.0.0.0"
    world_socket = socketUtils.socket_connect(world_hostname, 23456)
    initServer(engine, 0, world_socket)


    # orders = [Order(buyer = 2, product_id = 0, amount = 1, status = 'packed', rate = 1), 
    #           Order(buyer = 2, product_id = 1, amount = 1, status = 'packed', rate = 3), 
    #           Order(buyer = 2, product_id = 2, amount = 1, status = 'packed', rate = None), 
    #           Order(buyer = 2, product_id = 3, amount = 1, status = 'packed', rate = 5), 
    #           Order(buyer = 1, product_id = 4, amount = 1, status = 'packed', rate = 2), 
    #           Order(buyer = 1, product_id = 5, amount = 1, status = 'packed', rate = 6), 
    #           Order(buyer = 1, product_id = 0, amount = 1, status = 'packed', rate = 8), 
    #           Order(buyer = 1, product_id = 1, amount = 1, status = 'packed', rate = 1), 
    #           Order(buyer = 1, product_id = 2, amount = 1, status = 'packed', rate = 0), 
    #           ]

    # Session = sessionmaker(bind=engine)
    # session = Session()
    # for o in orders:
    #     session.add(o)
    # session.commit()
    # request.buy_product(1, 0, 10, (1,3))
    # Session = sessionmaker(bind=engine)

    # # create a session and query the data
    # session = Session()
    # users = session.query(User).all()

    # # print the usernames of all users
    # for user in users:
    #     print(user.username)