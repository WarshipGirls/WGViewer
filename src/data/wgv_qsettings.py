import os
import pickle

from ast import literal_eval



def del_key_file(key_file: str = '.wgr.key') -> None:
    if is_key_exists(key_file):
        os.remove(os.path.join(get_data_dir(), key_file))
    else:
        pass


def get_qsettings_file() -> str:
    return os.path.join(get_data_dir(), 'wgviewer.ini')


def get_key_path(key_file: str = '.wgr.key') -> str:
    return os.path.join(get_data_dir(), key_file)


def is_key_exists(key_file: str = '.wgr.key') -> bool:
    return os.path.exists(os.path.join(get_data_dir(), key_file))


def save_cookies(cookie: dict) -> None:
    from src.func.encryptor import Encryptor
    encryptor = Encryptor()
    key = encryptor.load_key(get_key_path())
    data = encryptor.encrypt_str(key, str(cookie))
    with open(os.path.join(get_data_dir(), 'user.cookies'), 'wb') as f:
        pickle.dump(data, f)


def load_cookies() -> dict:
    with open(os.path.join(get_data_dir(), 'user.cookies'), 'rb') as f:
        encrypted_cookie = pickle.load(f)
    if is_key_exists():
        try:
            from src.func.encryptor import Encryptor
            encryptor = Encryptor()
            key = encryptor.load_key(get_key_path())
            string = encryptor.decrypt_data(key, encrypted_cookie).decode('utf-8')
            res = literal_eval(string)
        except (AssertionError, AttributeError):
            res = {}
    else:
        res = {}
    return res


if __name__ == "__main__":
    from src.data.wgv_path import get_data_dir
else:
    from .wgv_path import get_data_dir

# End of File
