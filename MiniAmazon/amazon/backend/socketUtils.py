import io
import socket
from google.protobuf.internal.decoder import _DecodeVarint
from google.protobuf.internal.encoder import _EncodeVarint
import threading

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
    print("Send message : ")
    print(message)
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
    global lock
    buf = sock.recv(4)
    msg_length, hdr_length = _DecodeVarint(buf, 0)
    rsp_buffer = io.BytesIO()
    if hdr_length < 4:
        rsp_buffer.write(buf[hdr_length:])

    # read the remaining message bytes
    msg_length = msg_length - (4 - hdr_length)
    while msg_length > 0:
        rsp_bytes = sock.recv(min(8096, msg_length))
        rsp_buffer.write(rsp_bytes)
        msg_length = msg_length - len(rsp_bytes)
    return rsp_buffer.getvalue()