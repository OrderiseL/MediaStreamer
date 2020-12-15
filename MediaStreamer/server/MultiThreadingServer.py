import socket
import threading
import queue
import time
import general_functions as g_func
import server.server_functions as s_func

outgoingQ = queue.Queue()


class ThreadedServer(threading.Thread):
    # Defines a server thread that
    def __init__(self, host, port, q):
        super(ThreadedServer, self).__init__()
        # List of running processes.
        self.plist = []
        self.host = host
        self.port = port
        # Contains a queue of requests: (client,data_to_send).
        self.q = q
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        p = sendToClient(self.q)
        p.start()
        self.plist.append(p)

    # Gets connections to clients.
    def run(self):
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            p = listenToClient(client, address, self.plist, self.q)
            p.start()
            self.plist.append(p)


# Gets data from client and response to queue.
class listenToClient(threading.Thread):
    def __init__(self, client, address, plist, q):
        super(listenToClient, self).__init__()
        self.client = client
        self.client.settimeout(400)
        self.address = address
        self.plist = plist
        self.size = 1024 * 8
        self.q = q

    def run(self):
        print('running ', self.address)
        user_data = None
        msg = ''
        self.client.settimeout(400)
        while msg != 'done':
            try:
                msg = self.client.recv(self.size).decode()
                print(msg)
                if msg == 'login':  # log client in.
                    user_data = s_func.login(self.client)
                if msg == 'register':  # Create a new account.
                    user_data = s_func.signup(self.client)
                if msg == 'get':
                    s_func.send_files(self.client, user_data[2])
                if msg == 'uploading':  # video receive.
                    print('Action start')
                    g_func.rec_vid(self.client, user_data[2])
                if msg == 'download':  # Send video to client.
                    s_func.download(self.client, user_data[2])
            except socket.error as socketerror:
                print('Error:', socketerror)
                self.client.close()
                return False


# Sends each response in turn.
class sendToClient(threading.Thread):
    def __init__(self, q):
        super(sendToClient, self).__init__()

        self.size = 1024 * 8
        self.q = q

    def run(self):
        print('stat send process')
        while True:
            if not self.q.empty():
                message = self.q.get()
                message[0].send(message[1])
            time.sleep(0.1)


if __name__ == "__main__":
    port_num = 3000

    Ts = ThreadedServer('', port_num, outgoingQ)
    Ts.start()
    Ts.join()
