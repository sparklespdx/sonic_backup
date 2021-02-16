from Crypto.Cipher import AES
import base64
import os


def base64url_encode(payload):
    return base64.b64encode(payload).decode('utf-8').replace('/', '|')


def base64url_decode(payload):
    print(payload)
    return base64.b64decode(payload.decode('utf-8').replace('|', '/').encode())


def backup_file(path):
    config = Config()
    enc = Cryptor(config)
    remote = Remote(config, path)
    src = SourceFile(config, path)
    dst = DestinationFile(config, base64url_encode(enc.encrypt(path.encode())))

    backup_pipeline(src, enc, dst, remote)
    print(f"{dst.path}")


def backup_pipeline(src, enc, dst, remote):

    src.open_stream()
    dst.open_stream()

    while True:
        chunk = src.chunk()
        if chunk == b'':
            break
        cryptchunk = enc.encrypt(chunk)
        dst.write(cryptchunk)

    remote.send(dst)
    src.close_stream()
    dst.close_stream()


def restore_file(path):
    config = Config()
    enc = Cryptor(config)
    remote = Remote(config, path)
    dst = DestinationFile(config, enc.decrypt(base64url_decode(path.encode())).decode().split("/")[-1])
    src = SourceFile(config, path)

    restore_pipeline(src, enc, dst, remote)



def restore_pipeline(src, enc, dst, remote):
    src.open_stream()
    dst.open_stream()

    remote.get(src)

    while True:
        chunk = src.chunk()
        if chunk == b'':
            break
        plainchunk = enc.decrypt(chunk)
        dst.write(plainchunk)
    src.close_stream()
    dst.close_stream()


class Config:
    READ_CHUNK = int(5.243e6)
    ENC_KEY = b'\xea\x0f\xb6Y\x05\xda\xfc\x1e\xff\x0c\x05\xcdY\x92\x8a\x1d'

class Cryptor:

    def __init__(self, config):
        self.config = config
        self.cipher = AES.new(self.config.ENC_KEY, AES.MODE_EAX, nonce=b"foobaasdasdsadar")

    def encrypt(self, chunk):
        return self.cipher.encrypt(chunk)

    def decrypt(self, chunk):
        return self.cipher.decrypt(chunk)


class Remote:

    def __init__(self, config, path):
        self.config = config
        self.path = path

    def send(self, dst):
        return None

    def get(self, src):
        return None


class SourceFile:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.handle = None
        self.no_of_chunks = 0

    def open_stream(self):
        self.handle = open(self.path, "rb")

    def close_stream(self):
        self.handle.close()
        self.handle = None

    def chunk(self):
        self.no_of_chunks +- 1
        return self.handle.read(self.config.READ_CHUNK)


class DestinationFile:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.handle = None
        self.no_of_chunks = 0

    def open_stream(self):
        self.handle = open(self.path, "wb")

    def close_stream(self):
        self.handle.close()
        self.handle = None

    def write(self, data):
        return self.handle.write(data)
