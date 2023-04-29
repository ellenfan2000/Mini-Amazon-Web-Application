from amazon.backend.database import *
from amazon.backend import socketUtils, UPSMessage, WorldMessage, request, query, socketUtils
from amazon.backend import amazon_ups_pb2 as UPS
from amazon.backend import world_amazon_pb2 as WORLD
import socket

seqnum = 1

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 32345
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    sock.bind((local_ip, port))
    sock.listen()
    print(f"Server listening on {hostname}:{port}")
    amazon, address = sock.accept()
    print("connect to amazon")
    while True:
        if(amazon.fileno() == -1):
            print("Socket connection is closed.")
            break
        try:
            # command = UPS.ATUCommands()
            message = socketUtils.recv_message_v2(amazon)
            # print(message)
            command = UPS.ATUCommands()
            command.ParseFromString(message)
            print(command)
            for m in command.topickup:
                response = UPS.UTACommands()
                arrive = UPS.UTAArrived()
                arrive.packageid.append(m.packageid)
                arrive.truckid = 1
                arrive.whid = m.whid
                arrive.seqnum = seqnum + 1
                response.arrive.append(arrive)
                response.acks.append(m.seqnum)
                socketUtils.send_message(amazon, response)
        except Exception as e:
            print(e)

