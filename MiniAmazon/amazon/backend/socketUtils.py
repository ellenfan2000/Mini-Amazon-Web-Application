import io
import socket
from google.protobuf.internal.decoder import _DecodeVarint
from google.protobuf.internal.encoder import _EncodeVarint
import threading
import world_amazon_pb2 as WORLD
import amazon_ups_pb2 as UPS

lock = threading.Lock()


def socket_connect(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server's address and port
    server_address = (hostname, port)
    sock.connect(server_address)
    print("connect to " + hostname)
    return sock


def send_message(sock,message):
    global lock
    print("Send message : " + message.DESCRIPTOR.name)
    # print(message)
    message_str = message.SerializeToString()
    lock.acquire()
    _EncodeVarint(sock.send, len(message_str), None)
    sock.send(message_str)
    lock.release()

# def write_message_delimited(socket, msg):
#     hdr = []
#     _EncodeVarint(hdr.append, len(msg))
#     socket.sendall("".join(hdr))
#     socket.sendall(msg.SerializeToString())

def recv_message(sock):
    buf = sock.recv(4)
    if buf == b'':
        exit()
    msg_length, hdr_length = _DecodeVarint(buf, 0)
    rsp_buffer = io.BytesIO()
    if hdr_length < 4:
        rsp_buffer.write(buf[hdr_length:])

    # read the remaining message bytes
    msg_length = msg_length - (4 - hdr_length)
    while msg_length > 0:
        rsp_bytes = sock.recv(msg_length)
        rsp_buffer.write(rsp_bytes)
        msg_length = msg_length - len(rsp_bytes)
    return rsp_buffer.getvalue()

def recv_message_v2(sock):
    var_int_buff = []
    while True:
        buf = sock.recv(1)
        if buf == b'':
            exit()
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = sock.recv(msg_len)
    return whole_message

def recv_message_from_World(world_socket):
    world_reponse = WORLD.AResponses()
    world_reponse.ParseFromString(recv_message(world_socket))
    print("Recv message from World:")
    print(world_reponse)
    return world_reponse

def recv_message_from_UPS(ups_socket):
    ups_response = UPS.UTACommands()
    ups_response.ParseFromString(recv_message_v2(ups_socket))
    print("Recv message from UPS:")
    print(ups_response)
    return ups_response
