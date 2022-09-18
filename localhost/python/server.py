import socket
import selectors
import types

from functools import partial
from utils import HOST, PORT, SOCKSIZE

def accept_wrapper(sock: socket.socket, _, *, selector: selectors.BaseSelector) -> None:
    conn, addr = sock.accept()
    print(f"[INFO]: {addr} is connected.")
    sock.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)

def service_connection(key, mask, *, selector: selectors.BaseSelector) -> None:
    sock = key.fileobj
    data = key.data

    print("hi")

if __name__ == "__main__":

    sel = selectors.DefaultSelector()

    accept_func = partial(accept_wrapper, selector = sel)
    service_connection_func = partial(service_connection, selector = sel)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT)) # Bind host and port to socket
        sock.listen(1) # Queue size of pending connection is 1

        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        accept_func(key.fileobj, None) # type: ignore
                    else:
                        service_connection_func(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()