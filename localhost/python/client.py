import socket
import types
import selectors

from utils import HOST, PORT, SOCKSIZE

MESSAGES = [b"First Message from Client.", b"Second Message from Client."]

def generate_connections(nb: int = 10) -> None:
    for i in range(nb):
        print(f"[INFO]: Client {i} is ready to connect ...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)
            sock.connect_ex((HOST, PORT))
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=i,
                msg_total=sum(len(m) for m in MESSAGES),
                recv_total=0,
                messages=MESSAGES.copy(),
                outb=b"",
            )
            selector.register(sock, events, data=data)





if __name__ == "__main__":

    selector = selectors.DefaultSelector()

    generate_connections(10)