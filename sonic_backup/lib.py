from Crypto.Cipher import AES
import base64


class Config:
    READ_CHUNK = int(1024 * 500)
    ENC_KEY = b'\xea\x0f\xb6Y\x05\xda\xfc\x1e\xff\x0c\x05\xcdY\x92\x8a\x1d'
    SERVER_ADDR = "10.99.99.200"
    SERVER_PORT = 2222


def base64url_encode(payload):
    return base64.b64encode(payload).decode('utf-8').replace('/', '|')


def base64url_decode(payload):
    return base64.b64decode(payload.decode('utf-8').replace('|', '/').encode())


class CryptManager:

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
