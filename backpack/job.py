from Crypto.Cipher import AES
import base64
import os
import socket

def base64url_encode(payload):
    return base64.b64encode(payload).decode('utf-8').replace('/', '|')


def base64url_decode(payload):
    return base64.b64decode(payload.decode('utf-8').replace('|', '/').encode())


def backup_file(path):
    config = Config()

    enc = Crypto(config)
    remote = Remote(config)
    src = SourceFile(config, path)

    remote.send(src, enc)

    print(f"Sent: {src.path}")


def restore_file(path):
    config = Config()
    enc = Crypto(config)
    remote = Remote(config)

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


#def restore_pipeline(src, enc, dst, remote):
#    src.open_stream()
#    dst.open_stream()
#
#    remote.get(src)
#
#    while True:
#        chunk = src.chunk()
#        if chunk == b'':
#            break
#        plainchunk = enc.decrypt(chunk)
#        dst.write(plainchunk)
#    src.close_stream()
#    dst.close_stream()


class Config:
    READ_CHUNK = int(5.243e6)
    ENC_KEY = b'\xea\x0f\xb6Y\x05\xda\xfc\x1e\xff\x0c\x05\xcdY\x92\x8a\x1d'
    SERVER_ADDR = "10.99.99.200"
    SERVER_PORT = 2222

class Crypto:

    def __init__(self, config):
        self.config = config
        self.encrypt_cipher = AES.new(self.config.ENC_KEY, AES.MODE_EAX, nonce=b"foobaasdasdsadar")
        self.decrypt_cipher = AES.new(self.config.ENC_KEY, AES.MODE_EAX, nonce=b"foobaasdasdsadar")

    def encrypt(self, chunk):
        return self.encrypt_cipher.encrypt(chunk)

    def decrypt(self, chunk):
        return self.decrypt_cipher.decrypt(chunk)

    def cryptopath(self, path):
        return base64url_encode(self.encrypt(path))

    def originalpath(self, cryptopath):
        return self.decrypt(base64url_decode(cryptopath))


class Remote:

    def __init__(self, config):
        self.config = config
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        return self.socket.connect((self.config.SERVER_ADDR, self.config.SERVER_PORT))

    def bind(self):
        return self.socket.bind(("0.0.0.0", self.config.SERVER_PORT))

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

    def listen(self, dst):
        self.bind()
        self.socket.listen(1024)
        conn, addr = self.socket.accept()
        dst.open_stream()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                dst.write(data)
        dst.close_stream()
        self.close()


class SourceFile:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.no_of_chunks = 0

    def open_stream(self):
        self.handle = open(self.path, "rb")

    def close_stream(self):
        self.handle.close()

    def chunk(self):
        self.no_of_chunks +- 1
        return self.handle.read(self.config.READ_CHUNK)


class DestinationFile:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.no_of_chunks = 0

    def open_stream(self):
        self.handle = open(self.path, "ab")

    def close_stream(self):
        self.handle.close()

    def write(self, data):
        self.handle.write(data)
