import logging
import os
import platform

from pathlib import Path


# ================================
# Not Exports
# ================================


def _clear_dir(_dir):
    for filename in os.listdir(_dir):
        file_path = os.path.join(_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error('Failed to delete %s. Reason: %s' % (file_path, e))


# ================================
# Exports
# ================================


def clear_cache_folder():
    _clear_dir(get_data_dir())

def get_data_dir():
    # TODO: unix not tested
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

def get_init_dir():
    p = os.path.join(get_data_dir(), 'init')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p

def get_user_dir():
    p = os.path.join(get_data_dir(), 'user')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p

def get_temp_dir():
    p = os.path.join(get_data_dir(), 'temp')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p


# End of File