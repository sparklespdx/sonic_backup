import socket


class SonicServer:

    def __init__(self, config):
        self.config = config

    def listen(self, dst):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.config.SERVER_BIND_ADDR, self.config.SERVER_PORT))
        sock.listen()
        print(f"[***] Listening on {self.config.SERVER_BIND_ADDR}:{self.config.SERVER_PORT}...")
        conn, addr = sock.accept()
        print("[***] Connection accepted")
        dst.open_stream(mode='wb')
        with conn:
            while True:
                data = conn.recv(self.config.READ_CHUNK)
                if not data:
                    break
                dst.write(data)
        dst.close_stream()
        print("[***] Data written")
