import socket

from utils import HOST, PORT, SOCKSIZE


if __name__ == "__main__":

    server = socket.create_server((HOST, PORT), family = socket.AF_INET)

    server.listen(1)
    conn, add = server.accept()

    while True:
        data = conn.recv(SOCKSIZE)
        
        if data:
            print("New connection")