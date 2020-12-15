import socket, os, sys

"""CONSTANTS"""
BUFFSIZE = 2048
SUPPORTED_TYPES = ('mp3', 'mp4')
"""Functions that use sockets"""


# Func for receiving video.
def rec_vid(connection, storage):
    connection.send('ready'.encode())
    name = connection.recv(BUFFSIZE).decode('UTF8')
    file = storage + '\\' + name
    print(file)

    print("Starting to read bytes..")
    buffer = connection.recv(BUFFSIZE)
    with open(file, "wb") as video:
        while True:
            video.write(buffer)
            if 'done'.encode() in buffer:
                break
            buffer = connection.recv(BUFFSIZE)

    print('Video uploaded')
    return True


# Sends a video's name then reads video and sends every byte .
def upload_vid(connection, video_path):
    print("Sending:", video_path)
    # Checks files is a video and exists.
    if not os.path.isfile(video_path):
        print('File does\'nt exist')
        return
    # Sends file.
    connection.send('uploading'.encode())
    connection.recv(BUFFSIZE)
    vid_name = video_path.split('\\')[-1].encode()
    connection.send(vid_name)
    with open(video_path, "rb") as video:
        buffer = video.read()
        connection.sendall(buffer)
    connection.send('done'.encode())
    print("Done sending..")


if __name__ == '__main__':
    pass
