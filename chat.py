import socket
import threading
import sys

class Server:
    connections = []
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)

        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]), "connected")

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnectd")
                self.connections.remove(c)
                c.close()
                break

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        self.sock.connect((address, 1000))

        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))

if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()