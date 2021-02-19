from Crypto.Cipher import AES
import base64


class Config:
    # Size of chunks to read from and write to filesystem, in bytes.
    # 512kb
    READ_CHUNK = int(1024 * 512)

    # Size limit for metadata, in bytes.
    # Arbitrary data can be stored in here, but note that making the
    # metadata file too large may result in poor performance.
    # 64kb
    METADATA_SIZE = int(1024 * 64)

    # Encryption key. Do NOT store in server config, only client config.
    ENC_KEY = b'\xea\x0f\xb6Y\x05\xda\xfc\x1e\xff\x0c\x05\xcdY\x92\x8a\x1d'

    # Server network settings
    SERVER_ADDR = "10.99.99.200"
    SERVER_PORT = 2222
    SERVER_BIND_ADDR = "0.0.0.0"


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


class File:

    def __init__(self, config, path):
        self.config = config
        self.path = path
        self.no_of_chunks_read = 0
        self.no_of_chunks_write = 0

    def open_stream(self, mode='rb'):
        self.handle = open(self.path, mode)

    def close_stream(self):
        self.handle.close()

    def read_chunk(self):
        self.no_of_chunks_read +- 1
        return self.handle.read(self.config.READ_CHUNK)

    def write_chunk(self, chunk):
        self.no_of_chunks_write +- 1
        self.handle.write(chunk)


class ArchiveFile(File):

    def write_metadata(self, blob):
        if len(blob) != self.config.METADATA_SIZE:
            raise Exception(f"Metadata for {self.path} is {len(blob)} bytes, wrong size")
        self.open_stream('wb')
        self.handle.seek(0x600)
        self.handle.write(blob)
        self.handle.close()

    def read_metadata(self):
        self.open_stream('rb')
        # Seek past tar header and read metadata blob.
        self.handle.seek(0x600)
        blob = self.handle.read(self.config.METADATA_SIZE)
        self.close_stream()
        return blob