import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

def socket_connect(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server's address and port
    server_address = (hostname, port)
    sock.connect(server_address)
    print("connect to " + hostname)
    return sock


def send_message(world_socket,message):
    message_str = message.SerializeToString()
    _EncodeVarint(world_socket.send, len(message_str), None)
    world_socket.send(message_str)


def recv_message(world_socket):
    var_int_buff = []
    while True:
        buf = world_socket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = world_socket.recv(msg_len)
    return whole_message