
import socket

class Server:
    def __init__(self, port, buf_size):
        self.host = ''
        self.port = port
        self.buf_size = buf_size
        self.socket = None
        self.message_count = 0

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(4)  # backlog
        running = True
        while running:
            try:
                client, address = self.socket.accept()
                data = client.recv(self.buf_size)
                # the echo
                message = data.decode()
                self.message_count += 1
                print('Received message: "{}" (msg #{})'\
                    .format(message, self.message_count))
                client.send(self.gen_message(data, self.message_count))
            except OSError as e:
                print("OSError: ", e)
                running = False
            except KeyboardInterrupt:
                print(" Halting server due to keyboard interrupt.")
                running = False
            finally:
                client.close()

    def gen_message(self, data, n):
        return "{} (msg #{})"\
            .format(data.decode().upper(), n).encode()
