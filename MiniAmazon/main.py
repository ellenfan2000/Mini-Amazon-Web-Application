from amazon.backend.database import *
from amazon.backend import socketUtils,request, query
from amazon.backend.WorldMessage import WorldMessage
from amazon.backend.UPSMessage import UPSMessage
from amazon.backend import amazon_ups_pb2 as UPS
from amazon.backend import world_amazon_pb2 as WORLD
import socket
import threading
import struct
import time
from concurrent.futures import ThreadPoolExecutor

def connect_to_World(world_socket, wordid, session, world:WorldMessage):
    warehouses = [Warehouse(id=0, x=1, y=1),
                  Warehouse(id=1, x=2, y=2),
                  Warehouse(id=2, x=3, y=3)]
    
    connect = WORLD.AConnect()
    # connect.worldid = wordid
    for w in warehouses:
        # print(w.id, w.x, w.y)
        wh = world.create_Awarehouse(w.id, w.x, w.y)
        connect.initwh.append(wh)

    connect.isAmazon = True
    response = WORLD.AConnected()
    while (True):
        socketUtils.send_message(world_socket, connect)
        response_str = socketUtils.recv_message(world_socket)
        response.ParseFromString(response_str)
        print(response.result)
        if (response.result == "connected!"):
            print("Connected to World!")
            for wh in warehouses:
                session.add(wh)
            session.commit()
            return
        else:
            print(response.result)


def connect_to_UPS(ups_socket, world_id):
    auc = UPS.AUConnected()
    auc.worldid = world_id
    socketUtils.send_message(ups_socket, auc)
    print("Connected to UPS!")

def init_world(world_socket, session, world:WorldMessage):
    kindle = read_image('amazon/resource/kindle.jpg')
    lg = read_image('amazon/resource/LG.jpg')
    tulip = read_image('amazon/resource/Tulip.jpg')
    cloud = read_image('amazon/resource/cloud.jpg')
    women_coat = read_image('amazon/resource/women_coat.jpg')
    men_coat = read_image('amazon/resource/men_coat.jpg')
    facial_scream = read_image('amazon/resource/Facial_scream.jpg')
    dose_serum = read_image('amazon/resource/kiehls-dose-serum.jpg')
    products = [Products(id=0, name="Kindle Paperwhite (8 GB)", price=139.99, picture=kindle, category="Digital", inventory=500, warehouse_id=0),
                Products(id=1, name="LG 34\" LED Monitor", price=319.99,
                         picture=lg, category="Digital", inventory=200, warehouse_id=0),
                Products(id=2, name="WUZHOU Tulip Plush Toy", price=16.59,
                         picture=tulip, category="Toy", inventory=269, warehouse_id=1),
                Products(id=3, name="Jellycat Amuseables Cloud Plush", price=39.99,
                         picture=cloud, category="Top", inventory=340, warehouse_id=1),
                Products(id=4, name="Women's Open Front Knit Coat", price=69.99,
                         picture=women_coat, category="Cloth", inventory=189, warehouse_id=2),
                Products(id=5, name="Men's Notch Lapel Double Trench Coat", price=79.99,
                         picture=men_coat, category="Cloth", inventory=230, warehouse_id=2),
                Products(id=6, name="Kiehls Ultra Facial Cream", price=78.75,
                         picture=facial_scream, category="SkinCare", inventory=128, warehouse_id=2, description="Discover our #1 face cream formulated with 4.5% Squalane and Glacial Glycoprotein to strengthen your skin's moisture barrier for softer, smoother skin."),
                Products(id=7, name="Kiehls Micro-Dose Anti-Aging Retinol Serum",
                         price=48.75, picture=dose_serum, category="SkinCare", inventory=218, warehouse_id=2, description="A potent retinol serum in a daily-strength micro-dose that visibly reduces wrinkles, firms skin, evens skin tone, and smoothes texture with minimal discomfort. Paraben-free and fragrance-free."),
                ]

    command = WORLD.ACommands()

    for p in products:
        command.buy.append(world.create_APurchaseMore(
            p.warehouse_id, world.create_Aproduct(p.id, p.name, p.inventory)))
    command.disconnect = False

    while True:
        socketUtils.send_message(world_socket, command)
        print(command.DESCRIPTOR.name)
        for c in command.buy:
            print(c.seqnum)

        try:
            world_reponse = socketUtils.recv_message_from_World(world_socket)
            # world_reponse = WORLD.AResponses()
            # world_reponse.ParseFromString(socketUtils.recv_message(world_socket))

            # recieved acks, remove saved messages
            world.lock_resend.acquire()
            for i in world_reponse.acks:
                if (i in world.past_messages):
                    world.past_messages.pop(i)
            world.lock_resend.release()

            for i in world_reponse.error:
                print(i.err)

            for p in products:
                session.add(p)
            session.commit()

            print("World Initialized!")
            return
        except Exception as e:
            print(e)

def read_image(path):
    with open(path, 'rb') as f:
        data = f.read()
        return data
    
def initServer(session, ups_socket, world_socket, world:WorldMessage, ups:UPSMessage):
    uconnect = UPS.UTAConnect()
    # uconnect.ParseFromString(socketUtils.recv_message(ups_socket))
    uconnect.worldid = 1

    connect_to_World(world_socket, uconnect.worldid, session, world)
    init_world(world_socket, session, world)
    session.commit()
    # connect_to_UPS(ups_socket, uconnect.worldid)


def handle_world_response(world_socket, world:WorldMessage):
    print("Listening to all World response ...")
    while True:
        if(world_socket.fileno() == -1):
            print("Socket connection is closed.")
            break
        command = WORLD.ACommands()
        world_reponse = WORLD.AResponses()
        try:
            # world_reponse.ParseFromString(socketUtils.recv_message(world_socket))
            world_reponse = socketUtils.recv_message_from_World(world_socket)
            # if recieve ack, remove the command from the resend list
            world.lock_resend.acquire()
            for i in world_reponse.acks:
                if (i in world.past_messages):
                    world.past_messages.pop(i)
            world.lock_resend.release()

            # handle each type of message in response arrived
            for m in world_reponse.arrived:
                world.handle_APurchaseMore(m)
                command.acks.append(m.seqnum)
            for m in world_reponse.ready:
                world.handle_APacked(m)
                command.acks.append(m.seqnum)
            for m in world_reponse.loaded:
                world.handle_ALoaded(m)
                command.acks.append(m.seqnum)
            for m in world_reponse.packagestatus:
                world.handle_APackage(m)
                command.acks.append(m.seqnum)

            # send acks to world
            socketUtils.send_message(world_socket, command)

            for i in world_reponse.error:
                print(i.err)
            pass
        except Exception as e:
            print(e)


def handle_ups_response(ups_socket,world_socket,world:WorldMessage, ups:UPSMessage):
    print("Listening to all UPS response ...")
    thread_pool = ThreadPoolExecutor(max_workers=10)
    while True:
        try:
            command = UPS.ATUCommands()
            if(ups_socket.fileno() == -1 or world_socket.fileno() == -1):
                print("Socket connection is closed.")
                break
            ups_reponse = socketUtils.recv_message_from_UPS(ups_socket)
            # handle each type of message in response arrived
            for m in ups_reponse.arrive:
                command.acks.append(m.seqnum)
                thread_pool.submit(ups.handle_UTAArrived, world_socket,ups_socket, m, world)
            for m in ups_reponse.todeliver:
                command.acks.append(m.seqnum)
                ups.handle_UTAOutDelivery(m)
            for m in ups_reponse.delivered:
                command.acks.append(m.seqnum)
                ups.handle_Delivery(m)
            for i in ups_reponse.error:
                print(i.err)

            # send acks to UPS
            socketUtils.send_message(ups_socket, command)
        except Exception as e:
            print(e)

# resend message every 10 seconds
def handle_resend(world_socket, world:WorldMessage):
    while True:
        world.lock_resend.acquire()
        past_messages = world.past_messages
        command = WORLD.ACommands()
        for m in past_messages.values():
            if (m.DESCRIPTOR.name == 'APurchaseMore'):
                command.buy.append(m)
            elif (m.DESCRIPTOR.name == 'APack'):
                command.topack.append(m)
            elif (m.DESCRIPTOR.name == 'APutOnTruck'):
                command.load.append(m)
            elif (m.DESCRIPTOR.name == 'AQuery'):
                command.queries.append(m)
        world.lock_resend.release()
        socketUtils.send_message(world_socket, command)
        time.sleep(10)

def handle_front_end(ups_socket,world_socket,session, world:WorldMessage, ups:UPSMessage):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    port = 29081
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    sock.bind((local_ip, port))
    sock.listen()
    print(f"Server listening on {hostname}:{port}")

    while True:
        if(ups_socket.fileno() == -1 or world_socket.fileno() == -1):
            print("Socket connection is closed.")
            break
        # Accept incoming connection
        client_socket, client_address = sock.accept()
        d = client_socket.recv(4)
        package_id = struct.unpack('!I', d)[0]

        d = client_socket.recv(4)
        x = struct.unpack('!I', d)[0]

        d = client_socket.recv(4)
        y = struct.unpack('!I', d)[0]

        response = buy(package_id,x, y, ups_socket,world_socket,session, world, ups)

        length = struct.pack('!I', len(response))
        client_socket.sendall(length)
        client_socket.sendall(response.encode())
        client_socket.close()


def buy(package_id, x, y, ups_socket, world_socket, session, world:WorldMessage, ups:UPSMessage):
    print("Recieve order from front-end")
    Wcommand = WORLD.ACommands()
    order = session.query(Order).join(Order.product).filter(Order.package == package_id).first()

    # if inventory is not enough, send purchase more to world, return err message to client
    if(order.product.inventory < order.amount):
        Wcommand.buy.append(world.create_APurchaseMore(order.product.warehouse_id, world.create_Aproduct(order.product.id, order.product.name, 1000+2*order.amount)))
        order.status = 'canceled'
        session.commit()
        socketUtils.send_message(world_socket, Wcommand)
        return 'No enough inventory'
    session.commit()

    newpackage = Package(packageID = package_id, warehouse_id = order.product.warehouse_id, address_x = x, address_y = y)
    
    session.add(newpackage)
    session.commit()

    # send ATURequestPickUp, 
    print('Send request pick up to UPS')
    Ucommand = UPS.ATUCommands()
    Ucommand.topickup.append(ups.create_RequestPickUp(order.product.name, package_id, order.product.warehouse_id, x,y))
    socketUtils.send_message(ups_socket,Ucommand)

    # send Apacking
    print('Send request packing to World ')
    Wcommand.topack.append(world.create_APack(order.product.warehouse_id,package_id,world.create_Aproduct(order.product.id, order.product.name, order.amount)))
    socketUtils.send_message(world_socket,Wcommand)
    return 'Success'


'''
    protoc -I=./ --python_out=./ amazon_ups.proto
'''
if __name__ == '__main__':
    engine = initDataBase()
    # engine = getEngine()
    print("database initialized")
    ups_hostname = socket.gethostname()
    ups_socket = socketUtils.socket_connect(ups_hostname, 32346)

    world_hostname = "0.0.0.0"
    world_socket = socketUtils.socket_connect(world_hostname, 23456)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    world = WorldMessage(session)
    ups = UPSMessage(session)

    initServer(session, ups_socket, world_socket, world, ups)
    # # test_database(engine)


    # a thread waiting for all world response
    world_thread = threading.Thread(target=handle_world_response, args = (world_socket, world))
    world_thread.start()

    # a thread waiting for all ups response
    ups_thread = threading.Thread(target=handle_ups_response, args = (ups_socket, world_socket,world, ups))
    ups_thread.start()

    # a thread keep resending requests
    # resend_thread = threading.Thread(target = handle_resend, args = (world_socket, world))
    # resend_thread.start()

    # main threading handlind all buy request from clients
    handle_front_end(ups_socket,world_socket,session, world, ups)

    world_thread.join()
    ups_thread.join()
    # resend_thread.join()
    session.close()
    # test_database(engine)/\

# def test_database(engine):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     warehouses = [Warehouse(id=0, x=1, y=1),
#                   Warehouse(id=1, x=2, y=2),
#                   Warehouse(id=2, x=3, y=3)]

#     for wh in warehouses:
#         session.add(wh)
#     session.commit()

#     kindle = read_image('amazon/resource/kindle.jpg')
#     lg = read_image('amazon/resource/LG.jpg')
#     tulip = read_image('amazon/resource/Tulip.jpg')
#     cloud = read_image('amazon/resource/cloud.jpg')
#     women_coat = read_image('amazon/resource/women_coat.jpg')
#     men_coat = read_image('amazon/resource/men_coat.jpg')
#     facial_scream = read_image('amazon/resource/Facial_scream.jpg')
#     dose_serum = read_image('amazon/resource/kiehls-dose-serum.jpg')
#     products = [Products(id=0, name="Kindle Paperwhite (8 GB)", price=139.99, picture=kindle, category="Digital", inventory=500, warehouse_id=0),
#                 Products(id=1, name="LG 34\" LED Monitor", price=319.99,
#                          picture=lg, category="Digital", inventory=200, warehouse_id=0),
#                 Products(id=2, name="WUZHOU Tulip Plush Toy", price=16.59,
#                          picture=tulip, category="Toy", inventory=269, warehouse_id=1),
#                 Products(id=3, name="Jellycat Amuseables Cloud Plush", price=39.99,
#                          picture=cloud, category="Top", inventory=340, warehouse_id=1),
#                 Products(id=4, name="Women's Open Front Knit Coat", price=69.99,
#                          picture=women_coat, category="Cloth", inventory=189, warehouse_id=2),
#                 Products(id=5, name="Men's Notch Lapel Double Trench Coat", price=79.99,
#                          picture=men_coat, category="Cloth", inventory=230, warehouse_id=2),
#                 Products(id=6, name="Kiehls Ultra Facial Cream with Squalane", price=78.75,
#                          picture=facial_scream, category="SkinCare", inventory=128, warehouse_id=2, description="Discover our #1 face cream formulated with 4.5% Squalane and Glacial Glycoprotein to strengthen your skin's moisture barrier for softer, smoother skin."),
#                 Products(id=7, name="Kiehls Micro-Dose Anti-Aging Retinol Serum with Ceramides and Peptide",
#                          price=48.75, picture=dose_serum, category="SkinCare", inventory=218, warehouse_id=2, description="A potent retinol serum in a daily-strength micro-dose that visibly reduces wrinkles, firms skin, evens skin tone, and smoothes texture with minimal discomfort. Paraben-free and fragrance-free."),
#                 ]

#     for p in products:
#         session.add(p)
#     session.commit()

#     orders = [Order(buyer=2, product_id=0, amount=1, status='packed', package=101, rate=1, comment="not good"),
#               Order(buyer=2, product_id=1, amount=1, status='packed',
#                     package=102, rate=3, comment="not bad"),
#               Order(buyer=2, product_id=2, amount=1, status='packed',
#                     package=103, rate=None, comment="just soso"),
#               Order(buyer=2, product_id=3, amount=1, status='packed',
#                     package=104, rate=5, comment="not as expected"),
#               Order(buyer=1, product_id=4, amount=1, status='packed',
#                     package=105, rate=2, comment="not good enough on my standard"),
#               Order(buyer=1, product_id=5, amount=1, status='packed',
#                     package=106, rate=6, comment="feel nice"),
#               Order(buyer=1, product_id=0, amount=1, status='packed',
#                     package=107, rate=8, comment="it looks very good"),
#               Order(buyer=1, product_id=1, amount=1, status='packed',
#                     package=108, rate=1, comment="ahahahah"),
#               Order(buyer=1, product_id=2, amount=1, status='packed',
#                     package=109, rate=0, comment="heyhey"),
#               ]

#     package_id = 100

#     for o in orders:
#         session.add(o)
#         package_id += 1
#         session.add(Package(packageID=package_id,
#                     warehouse_id=0, address_x=1, address_y=1))

#     session.commit()
#     # request.buy_product(1, 0, 10, (1,3))
#     # query.get_product_detail(0)


