"""
This is the module that implements the online serving of the app.
"""
import socket
import threading
from typing import Optional, Tuple

from server.server_consts import TELNET_PORT, MAX_CONNECTIONS


class ServerInstance(threading.Thread):
    def __init__(self, socket_address_tuple: Tuple[socket.socket, Tuple[int, int]]):
        super(ServerInstance, self).__init__()
        self.socket = socket_address_tuple[0]
        self.address = socket_address_tuple[1]

    def run(self):
        print('{} connected.'.format(self.address))
        while True:
            data = self.socket.recv(1024)
            print(data)


def run_server(port: Optional[int] = None, debug: Optional[bool] = False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1" if debug else ""
    if port is None:
        port = TELNET_PORT
    s.bind((host, port))
    s.listen(MAX_CONNECTIONS)

    while True:
        ServerInstance(s.accept()).start()


if __name__ == '__main__':
    run_server()
