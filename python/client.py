import socket

from utils import HOST, PORT

if __name__ == "__main__":

    conn = socket.create_connection((HOST, PORT))