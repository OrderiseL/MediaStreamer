import socket, os, sys, pickle, general_functions as g_func
from server.registerLogin import RegisterLogin

"""CONSTANTS"""
BUFFSIZE = 2048
# REGISTER FLAGS
PASSWORD = 0
RECOVERY_EMAIL = 1
IS_LOGGED = 2
LAST_LOGIN = 3
USER_ALREADY_EXISTS = 11
USER_ADDED = 10
LOGIN_SUCCESS = 12

USER_NOT_EXIST = 14
LOGOUT_SUCCESS = 15
USER_ALREADY_LOGGED_OUT = 16
MAX_LOGIN_COUNT = 5
"""Functions"""


def login(client):
    print('login Start')
    client.send('ready'.encode())

    info = pickle.loads(client.recv(BUFFSIZE))
    print(info)
    username, psf = info
    u = RegisterLogin()
    res, user_data = u.login(username, psf)
    if res == LOGIN_SUCCESS:
        print('logged in.')
        client.send('success'.encode())
        return user_data
    else:
        client.send('fail'.encode())
        return


def signup(client):
    print('Registration Start')
    client.send('ready'.encode())

    info = pickle.loads(client.recv(BUFFSIZE))
    print(info)
    username, psf = info
    u = RegisterLogin()
    res, user_data = u.register(username, psf)
    if res == USER_ADDED:
        print(user_data, 'Added')
        client.send('success'.encode())
        return user_data
    else:
        client.send('fail'.encode())
        return


def send_files(client, storage):
    print('Sending files')
    files = os.listdir(storage)
    print('sending:', files)
    files = pickle.dumps(files)
    client.send(files)


def download(client, storage):
    client.send('ready'.encode())
    name = client.recv(BUFFSIZE).decode()
    print(name)
    if name == 'finish':
        return
    path = storage + '\\' + name
    g_func.upload_vid(client, path)


if __name__ == '__main__':
    pass
