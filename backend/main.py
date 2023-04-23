from database import *
import socket
import socketUtils
import UPSMessage
import WorldMessage
import amazon_ups_pb2 as UPS
import world_amazon_pb2 as World




'''
    protoc -I=./ --python_out=./ amazon_ups.proto
    '''
if __name__ == '__main__':
    engine = init()
    # ups_hostname = "0.0.0.0"
    # ups_socket = socketUtils.socket_connect(ups_hostname, 32345)

    # uconnect= UPS.UTAConnect()
    # uconnect.ParseFromString(socketUtils.recv_message(ups_socket))

    world_hostname = "0.0.0.0"
    world_socket = socketUtils.socket_connect(world_hostname, 23456)
    WorldMessage.connect_to_World(world_socket,1,4)
    # WorldMessage.connect_to_World(world_socket,uconnect.worldid,4)
    WorldMessage.init_world(world_socket)
    

    # Session = sessionmaker(bind=engine)

    # # create a session and query the data
    # session = Session()
    # users = session.query(User).all()

    # # print the usernames of all users
    # for user in users:
    #     print(user.username)