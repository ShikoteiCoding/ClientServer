import socket

from utils import HOST, PORT, SOCKSIZE

if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(b"I am a client.")
        data = sock.recv(SOCKSIZE)

    print(f"Receivef: {data}")