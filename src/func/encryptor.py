import logging

from cryptography.fernet import Fernet


class Encryptor:
    def __init__(self):
        pass

    @staticmethod
    def gen_key():
        return Fernet.generate_key()

    @staticmethod
    def save_key(key, path):
        with open(path, 'wb') as f:
            f.write(key)

    @staticmethod
    def load_key(path):
        with open(path, 'rb') as f:
            key = f.read()
        return key

    @staticmethod
    def encrypt_str(key, string):
        return Fernet(key).encrypt(bytes(string, encoding='utf8'))

    @staticmethod
    def decrypt_data(key, data):
        try:
            return Fernet(key).decrypt(data)
        except TypeError:
            logging.error('Key file or config file corrupted.')
            return False


# End of File
