from database import *
import socket
import socketUtils
if __name__ == '__main__':
    engine = init()
    ups_hostname = "0.0.0.0"
    ups_socket = socketUtils.socket_connect(ups_hostname, 32345)

    '''
    protoc -I=./ --python_out=./ amazon_ups.proto
    '''

    # Session = sessionmaker(bind=engine)

    # # create a session and query the data
    # session = Session()
    # users = session.query(User).all()

    # # print the usernames of all users
    # for user in users:
    #     print(user.username)