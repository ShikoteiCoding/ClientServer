import socket
import types
import selectors

from functools import partial
from utils import HOST, PORT, SOCKSIZE

MESSAGES = [b"First Message from Client.", b"Second Message from Client."]

def generate_connections(selector, nb: int = 10) -> None:
    for i in range(nb):
        print(f"[INFO]: Client {i} is ready to connect ...")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

def handle_event_func(key, mask, selector: selectors.BaseSelector):
     sock: socket.socket = key.fileobj #type: ignore
     data = key.data

     if mask & selectors.EVENT_READ:
        recv_data = sock.recv(SOCKSIZE)
        if recv_data:
            print(f"[INFO]: Receiving data for client {data.connid} ...")
            print(f"[INFO]: Data is: {recv_data}")
            data.recv_total += len(recv_data)

        if not recv_data or not data.recv_total == data.msg_total:
            print(f"[INFO]: Closing connection for client {data.connid} ...")
            selector.unregister(sock)
            sock.close()

     if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]



if __name__ == "__main__":

    selector = selectors.DefaultSelector()

    generate_connections(selector, 10)

    handle_event = partial(handle_event_func, selector=selector)

    try:
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data:
                    handle_event(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        selector.close()