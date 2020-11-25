from cryptography.fernet import Fernet


class Encryptor():
    def __init__(self):
        pass

    def gen_key(self):
        return Fernet.generate_key()

    def save_key(self, key, path):
        with open(path, 'wb') as mykey:
            mykey.write(key)

    def load_key(self, path):
        with open(path, 'rb') as mykey:
            key = mykey.read()
        return key

    def encrypt_str(self, key, string):
        return Fernet(key).encrypt(bytes(string, encoding='utf8'))

    def decrypt_data(self, key, data):
        return Fernet(key).decrypt(data)


# End of File