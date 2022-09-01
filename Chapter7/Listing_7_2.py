from threading import Thread
import socket


class ClientEchoThread(Thread):
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client: socket.socket = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)

                # If there is no data, raise an exception. This happens when the connection was closed by the client or the connection was shut down.
                if not data:
                    raise BrokenPipeError('Connection closed!')

                print(f'Received {data}, sending!')

                self.client.sendall(data)
        except OSError as e:
            # When we have an exception, exit the run method. This terminates the thread.
            print(f'Thread interrupted by {e} exception, shutting down !')

    def close(self):
        # Shut down the connection if the thread is alive; the thread may not be alive if the client closed the connection
        if self.is_alive():
            self.client.sendall(bytes('Shutting down!', encoding='utf-8'))

            # Shut down the client connection for reads and writes.
            self.client.shutdown(socket.SHUT_RDWR)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen()
    connection_threads = []

    try:
        while True:
            connection, addr = server.accept()
            thread = ClientEchoThread(connection)
            connection_threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print('Shutting down')

        # Call the close method on our threads to shut down each client connection on keyboard interrupt.
        [thread.close() for thread in connection_threads]