import logging
import os
import platform
import shutil

from typing import Tuple

from pathlib import Path
from datetime import date


# ================================
# Not Exports
# ================================


def _clear_dir(_dir: str, is_all: bool = False) -> bool:
    if is_all is True:
        skips = []
    else:
        skips = ['log', 'zip']
    for filename in os.listdir(_dir):
        if filename in skips:
            continue
        else:
            pass
        file_path = os.path.join(_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error('Failed to delete %s. Reason: %s' % (file_path, e))
            return False
    return True


# ================================
# Exports
# ================================


def clear_cache_folder(is_all: bool = False) -> bool:
    return _clear_dir(get_data_dir(), is_all)


def get_data_dir() -> str:
    # TODO: mac not tested
    plt = platform.system()
    _dir = ''
    if plt == "Windows":
        _dir = os.getenv('LOCALAPPDATA')
    elif plt == "Linux":
        _dir = os.path.join(str(Path.home()), '.config')
    elif plt == "Darwin":
        _dir = os.path.join(str(Path.home()), 'Library', 'Application Support')
    else:
        _dir = str(Path.home())
    return os.path.join(_dir, 'WarshipGirlsViewer')


def get_init_dir() -> str:
    p = os.path.join(get_data_dir(), 'zip', 'init')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p


def get_log_dir() -> str:
    p = os.path.join(get_data_dir(), 'logs')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p


def get_expedition_log() -> Tuple[str, str]:
    # local timezone
    t = list(map(str, date.today().isocalendar()))
    dir_path = os.path.join(get_log_dir(), t[0], t[1])
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    else:
        pass

    return os.path.join(dir_path, 'week.csv'), os.path.join(dir_path, f'{t[2]}.csv')


def get_temp_dir() -> str:
    p = os.path.join(get_data_dir(), 'temp')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p


def get_user_dir() -> str:
    p = os.path.join(get_data_dir(), 'user')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p


def get_zip_dir() -> str:
    p = os.path.join(get_data_dir(), 'zip')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p

# End of File
