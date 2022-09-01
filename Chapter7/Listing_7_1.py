from threading import Thread
import socket


def echo(client: socket.socket):
    while True:
        data = client.recv(2048)
        print(f'Received {data}, sending!')
        client.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen()

    while True:
        # Block waiting for a client to connect
        connection, _ = server.accept()

        # Once a client connects, create a thread to run our echo function.
        thread = Thread(target=echo, args=(connection,))

        # Start running the thread
        thread.start()
