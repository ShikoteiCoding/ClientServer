import socket

from utils import HOST, PORT


if __name__ == "__main__":

    server = socket.create_server((HOST, PORT), family = socket.AF_INET)