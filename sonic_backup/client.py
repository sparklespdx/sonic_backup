import socket
from sonic_backup.lib import Config, CryptManager, SourceFile, DestinationFile

def backup_file(config, path):

    enc = CryptManager(config)
    remote = SonicClient(config)
    src = SourceFile(config, path)

    print("[***] Sending to backup server...")
    remote.send(src, enc)

    print(f"[***] Backed Up: {src.path}")


def restore_file(path):
    config = Config()
    enc = CryptManager(config)
    remote = SonicClient(config)

    cryptpath = enc.cryptopath(path)
    dst = DestinationFile(config, path)
    src = SourceFile(config, cryptpath)

    src.open_stream()
    dst.open_stream()
    while True:
        chunk = src.chunk()
        if chunk == b'':
            break
        dst.write(enc.decrypt(chunk))


    src.close_stream()
    dst.close_stream()

    print(f"Restored: {dst.path}")


class SonicClient:

    def __init__(self, config):
        self.config = config
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        return self.socket.connect((self.config.SERVER_ADDR, self.config.SERVER_PORT))

    def close(self):
        self.socket.close()

    def send(self, src, enc):
        self.connect()

        total_sent = 0
        chunk = None
        src.open_stream()
        while chunk != b'':
            chunk = src.chunk()
            cryptchunk = enc.encrypt(chunk)
            sent = self.socket.sendall(cryptchunk)
            if sent == 0:
                raise RuntimeError("socket connection broken")
            #data = self.socket.recv(1024)
        src.close_stream()
        self.close()

