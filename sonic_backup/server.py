import socket

class SonicServer:

    def __init__(self, config):
        self.config = config

    def listen(self, dst):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", self.config.SERVER_PORT))
        sock.listen()
        print("[***] Listening on 0.0.0.0:{self.config.SERVER_PORT}...")
        conn, addr = sock.accept()
        print("[***] Connection accepted")
        dst.open_stream()
        with conn:
            while True:
                data = conn.recv(1024 * 500)
                if not data:
                    break
                dst.write(data)
        dst.close_stream()
        print("[***] Data written")
