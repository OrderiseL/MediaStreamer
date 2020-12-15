import socket, os, sys, pickle, general_functions as g_func
from tkinter import *

"""CONSTANTS"""
BUFFSIZE = 2048
"""Functions"""


def login(client, username, password, root):
    client.send('login'.encode())
    info = pickle.dumps((username, password))
    client.recv(BUFFSIZE)  # Wait 'till server's ready.
    client.send(info)
    result = client.recv(BUFFSIZE).decode()  # Check if login successful
    if result == 'success':
        print('login success')
        root.destroy()
        return 'success'
    else:
        return 'wrong username or password'


def signup(client, username, password, root):
    client.send('register'.encode())
    info = pickle.dumps((username, password))
    client.recv(BUFFSIZE)  # Wait 'till server's ready.
    client.send(info)
    result = client.recv(BUFFSIZE).decode()  # Check if signup successful
    if result == 'success':
        print('Signup success')
        root.destroy()
        return 'success'
    else:
        return 'User exists'


def download(client, filename, storage):
    client.send('download'.encode())
    client.recv(BUFFSIZE)
    client.send(filename.encode())
    if client.recv(BUFFSIZE).decode() == 'uploading':
        g_func.rec_vid(client, storage)
        print('Download complete')


def get_files(client):
    print('getting files')
    client.send('get'.encode())
    files = pickle.loads(client.recv(BUFFSIZE))
    return files


def play_a_file(client, filename, storage):
    if filename in os.listdir(storage):
        os.startfile(storage+'\\' + filename)
    else:
        download(client, filename, storage)
        os.startfile(storage + '\\' + filename)


if __name__ == '__main__':
    pass
