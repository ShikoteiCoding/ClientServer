import socket

from utils import HOST, PORT, SOCKSIZE


if __name__ == "__main__":

    server = socket.create_server((HOST, PORT), family = socket.AF_INET)

    server.listen(1)
    conn, add = server.accept()

    with conn:
        print(f"{add} is connected.")
        while True:
            data = conn.recv(SOCKSIZE)
            
            if not data : break

            conn.sendall(data)