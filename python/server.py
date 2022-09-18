import socket

from utils import HOST, PORT, SOCKSIZE


if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))

        sock.listen(1) # Queue size of pending connection is 1
        conn, addr = sock.accept()

        with conn:
            print(f"[INFO]: {addr} is connected.")

            while True:
                data = conn.recv(SOCKSIZE)
                
                if not data : break
                
                conn.sendall(data + b". From server.")