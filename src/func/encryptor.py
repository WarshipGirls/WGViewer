from typing import Union

from cryptography.fernet import Fernet

from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger

logger = get_logger(QLOGS.FUNC)


class Encryptor:
    def __init__(self):
        pass

    @staticmethod
    def gen_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def save_key(key: bytes, path: str) -> None:
        with open(path, 'wb') as f:
            f.write(key)

    @staticmethod
    def load_key(path: str) -> bytes:
        with open(path, 'rb') as f:
            key = f.read()
        return key

    @staticmethod
    def encrypt_str(key: bytes, string: str):
        return Fernet(key).encrypt(bytes(string, encoding='utf8'))

    @staticmethod
    def decrypt_data(key: bytes, data: bytes) -> Union[bytes, None]:
        try:
            return Fernet(key).decrypt(data)
        except TypeError:
            logger.error('Key file or config file corrupted.')
            return None

# End of File
