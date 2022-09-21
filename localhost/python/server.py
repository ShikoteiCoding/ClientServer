import socket
import selectors
import types

from functools import partial
from utils import HOST, PORT, SOCKSIZE

def accept_func(sock: socket.socket, _, *, selector: selectors.BaseSelector) -> None:
    conn, addr = sock.accept()
    print(f"[INFO]: {addr} is connected.")
    sock.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    event = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, event, data=data)

def handler_connection_func(key, mask, *, selector: selectors.BaseSelector) -> None:
    sock: socket.socket = key.fileobj 
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(SOCKSIZE)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"[INFO]: Closing connection to {data.addr}...")
            selector.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"[INFO]: Echoing {data.outb!r} to {data.addr}...")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

if __name__ == "__main__":

    selector = selectors.DefaultSelector()

    accept = partial(accept_func, selector=selector)
    handler_connection = partial(handler_connection_func, selector=selector)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.bind((HOST, PORT)) # Bind host and port to socket
        sock.listen() # Queue size of pending connection is 1

        print(f"[INFO]: Server is listening... Ready to accept connections on {HOST, PORT}.")

        sock.setblocking(False)
        selector.register(sock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = selector.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        accept(key.fileobj, None) # type: ignore
                    else:
                        handler_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            selector.close()