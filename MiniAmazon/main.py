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
import threading
from PIL import Image

def connect_to_World(world_socket,wordid,warehouses):
    connect = WORLD.AConnect()
    # connect.worldid = wordid
    for w in warehouses:
        print(w.id, w.x, w.y)
        wh = WorldMessage.create_Awarehouse(w.id, w.x, w.y)
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

def connect_to_UPS(ups_socket, world_id):
    auc = UPS.AUConnected()
    auc.worldid = world_id
    socketUtils.send_message(ups_socket, auc)

def init_world(world_socket, session, products):
    command = WORLD.ACommands()
    for p in products:
        command.buy.append(WorldMessage.create_APurchaseMore(p.warehouse_id, WorldMessage.create_Aproduct(p.id, p.name, p.inventory)))
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

            for p in products:
                session.add(p)
            session.commit()
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
    
    uconnect= UPS.UTAConnect()
    # uconnect.ParseFromString(socketUtils.recv_message(ups_socket))
    uconnect.worldid = 1

    connect_to_World(world_socket,uconnect.worldid,warehouses)
    for wh in warehouses:
        session.add(wh)
    session.commit()

    init_world(world_socket, session, products)
    # for p in products:
    #     session.add(p)
    session.commit()
    # UPSMessage.connect_to_UPS(ups_socket, uconnect.worldid)



def handle_world_response(world_socket, session):
    while True:
        command = WORLD.ACommands()
        world_reponse = WORLD.AResponses()
        world_reponse.ParseFromString(socketUtils.recv_message(world_socket))

        # if recieve ack, remove the command from the resend list
        for i in world_reponse.acks:
            if(i in WorldMessage.past_messages):
                WorldMessage.past_messages.pop(i)

        # handle each type of message in response arrived
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

        # send acks to world 
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


def test_database(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    warehouses = [Warehouse(id = 0, x = 1, y = 1),
                  Warehouse(id = 1, x = 2, y = 2),
                  Warehouse(id = 2, x = 3, y = 3)]
    
    for wh in warehouses:
        session.add(wh)
    session.commit()

    kindle =Image.open('./amazon/resource/kindle.jpg').tobytes()
    lg = Image.open('./amazon/resource/LG.jpg').tobytes()
    tulip = Image.open('./amazon/resource/Tulip.jpg').tobytes()
    cloud = Image.open('./amazon/resource/cloud.jpg').tobytes()
    women_coat = Image.open('./amazon/resource/women_coat.jpg').tobytes()
    men_coat = Image.open('./amazon/resource/men_coat.jpg').tobytes()
    
    products =[Products(id = 0, name = "Kindle Paperwhite (8 GB)", price =139.99, picture = kindle, category = "Digital", inventory = 500, warehouse_id= 0),
               Products(id = 1, name = "LG 34\" LED Monitor", price = 319.99, picture = lg, category = "Digital", inventory = 200, warehouse_id= 0),
               Products(id = 2, name = "WUZHOU Tulip Plush Toy", price = 16.59, picture = tulip, category ="Toy", inventory = 269, warehouse_id= 1),
               Products(id = 3, name = "Jellycat Amuseables Cloud Plush", price = 39.99, picture = cloud, category = "Top", inventory = 340, warehouse_id= 1),
               Products(id = 4, name = "Women's Open Front Knit Coat", price = 69.99, picture = women_coat, category = "Cloth", inventory = 189, warehouse_id= 2),
               Products(id = 5, name = "Men's Notch Lapel Double Trench Coat", price = 79.99, picture = men_coat, category = "Cloth", inventory = 230, warehouse_id= 2)
               ]
    
    for p in products:
        session.add(p)
    session.commit()

    orders = [Order(buyer=2, product_id=0, amount=1, status='packed', package=101, rate=1, comment = "not good"),
              Order(buyer=2, product_id=1, amount=1, status='packed', package=102, rate=3, comment = "not bad"),
              Order(buyer=2, product_id=2, amount=1, status='packed', package=103, rate=None, comment = "just soso"),
              Order(buyer=2, product_id=3, amount=1, status='packed', package=104, rate=5, comment = "not as expected"),
              Order(buyer=1, product_id=4, amount=1, status='packed', package=105, rate=2, comment = "not good enough on my standard"),
              Order(buyer=1, product_id=5, amount=1, status='packed', package=106, rate=6, comment = "feel nice"),
              Order(buyer=1, product_id=0, amount=1, status='packed', package=107, rate=8, comment = "it looks very good"),
              Order(buyer=1, product_id=1, amount=1, status='packed', package=108, rate=1, comment = "ahahahah"),
              Order(buyer=1, product_id=2, amount=1, status='packed', package=109, rate=0, comment = "heyhey"),
              ]

    
    for o in orders:
        session.add(o)
        package_id += 1
        session.add(Package(packageID=package_id,
                    warehouse_id=0, address_x=1, address_y=1))

    session.commit()
    # request.buy_product(1, 0, 10, (1,3))
    # query.get_product_detail(0)

if __name__ == '__main__':
    engine = initDataBase()
    # engine = getEngine()
    # print("database initialized")
    # # ups_hostname = "0.0.0.0"
    # # ups_socket = socketUtils.socket_connect(ups_hostname, 32345)

    # world_hostname = "0.0.0.0"
    # world_socket = socketUtils.socket_connect(world_hostname, 23456)
    # initServer(engine, 0, world_socket)
    # # test_database(engine)
    # # Create a new thread

    # Session = sessionmaker(bind=engine)
    # session = Session()
    # world_thread = threading.Thread(target=handle_world_response(world_socket, session))
    # world_thread.start()


    # # Do some other work in the main thread
    # print("This is the main thread.")

    # # Wait for the thread to finish (optional)
    # world_thread.join()

    test_database(engine)