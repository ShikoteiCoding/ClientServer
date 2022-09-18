import socket

from utils import HOST, PORT, SOCKSIZE


if __name__ == "__main__":

    with socket.create_server((HOST, PORT), family = socket.AF_INET) as sock:
        
        sock.listen(1) # Queue size of pending connection is 1
        conn, addr = sock.accept()

        with conn:
            print(f"[INFO]: {addr} is connected.")

            while True:
                data = conn.recv(SOCKSIZE)
                
                if not data : break
                
                conn.sendall(data + b". From server.")