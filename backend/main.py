from database import *

if __name__ == '__main__':
    engine = init()
    Session = sessionmaker(bind=engine)

    # create a session and query the data
    session = Session()
    users = session.query(User).all()

    # print the usernames of all users
    for user in users:
        print(user.username)