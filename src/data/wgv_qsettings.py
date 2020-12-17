import os
import pickle

import qdarkstyle

from ast import literal_eval

from PyQt5.QtCore import QSettings

from src.func.encryptor import Encryptor
from src.func import qsettings_keys as QKEYS


def del_key_file(key_file: str = '.wgr.key') -> None:
    if is_key_exists(key_file):
        os.remove(os.path.join(get_data_dir(), key_file))
    else:
        pass


def get_color_option() -> str:
    return qsettings.value(QKEYS.STYLE) if qsettings.contains(QKEYS.STYLE) else "qdarkstyle"


def get_color_scheme() -> str:
    if get_color_option() == "native":
        return ""
    else:
        qsettings.setValue(QKEYS.STYLE, "qdarkstyle")
        return qdarkstyle.load_stylesheet(qt_api='pyqt5')


def get_qsettings_file() -> str:
    return os.path.join(get_data_dir(), 'wgviewer.ini')


def get_key_path(key_file: str = '.wgr.key') -> str:
    return os.path.join(get_data_dir(), key_file)


def is_key_exists(key_file: str = '.wgr.key') -> bool:
    return os.path.exists(os.path.join(get_data_dir(), key_file))


def save_cookies(cookie: dict) -> None:
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

    qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
else:
    from .wgv_path import get_data_dir

    qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)

# End of File
