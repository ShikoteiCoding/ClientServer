import socket

from utils import HOST, PORT, SOCKSIZE

if __name__ == "__main__":

    with socket.create_connection((HOST, PORT)) as s:
        s.sendall(b"I am a client.")
        data = s.recv(SOCKSIZE)

    print(f"Receivef: {data}")