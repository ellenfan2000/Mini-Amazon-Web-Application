from database import *
import socket
import socketUtils
import UPSMessage
import WorldMessage
import amazon_ups_pb2 as UPS
import world_amazon_pb2 as World


def initServer(engine, ups_socket, world_socket):
    Session = sessionmaker(bind=engine)
    session = Session()
    warehouses = [Warehouse(id = 0, x = 1, y = 1),
                  Warehouse(id = 1, x = 2, y = 2),
                  Warehouse(id = 2, x = 3, y = 3)]
    
    products =[Products(id = 0, name = "Kindle Paperwhite (8 GB)", price =139.99, category = "Digital", inventory = 500, warehouse= 0),
               Products(id = 1, name = "LG 34\" LED Monitor", price = 319.99, category = "Digital", inventory = 200, warehouse= 0),
               Products(id = 2, name = "WUZHOU Tulip Plush Toy", price = 16.59, category ="Toy", inventory = 269, warehouse= 1),
               Products(id = 3, name = "Jellycat Amuseables Cloud Plush", price = 39.99, category = "Top", inventory = 340, warehouse= 1),
               Products(id = 4, name = "Women's Open Front Knit Coat", price = 69.99, category = "Cloth", inventory = 189, warehouse= 2),
               Products(id = 5, name = "Men's Notch Lapel Double Trench Coat", price = 79.99, category = "Cloth", inventory = 230, warehouse= 2)
               ]
    
    # uconnect= UPS.UTAConnect()
    # uconnect.ParseFromString(socketUtils.recv_message(ups_socket))

    WorldMessage.connect_to_World(world_socket,1,warehouses)
      # WorldMessage.connect_to_World(world_socket,uconnect.worldid,warehouses)
    for wh in warehouses:
        session.add(wh)
    session.commit()

    WorldMessage.init_world(world_socket, products)
    for p in products:
        session.add(p)
    session.commit()

'''
    protoc -I=./ --python_out=./ amazon_ups.proto
'''
if __name__ == '__main__':
    engine = initDataBase()
    print("database initialized")
    # ups_hostname = "0.0.0.0"
    # ups_socket = socketUtils.socket_connect(ups_hostname, 32345)

    world_hostname = "0.0.0.0"
    world_socket = socketUtils.socket_connect(world_hostname, 23456)
    initServer(engine, 0, world_socket)

    # Session = sessionmaker(bind=engine)

    # # create a session and query the data
    # session = Session()
    # users = session.query(User).all()

    # # print the usernames of all users
    # for user in users:
    #     print(user.username)