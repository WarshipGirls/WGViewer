import os
import qdarkstyle

from PyQt5.QtCore import QSettings

from .wgv_path import _get_data_dir


def get_color_scheme():
    qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
    s = qsettings.value("style") if qsettings.contains("style") else "qdarkstyle"
    if s == "native":
        return ""
    else:
        qsettings.setValue("style", "qdarkstyle")
        return qdarkstyle.load_stylesheet(qt_api='pyqt5')

def get_qsettings_file():
    return os.path.join(_get_data_dir(), 'wgviewer.ini')

def get_key_path(key_file):
    return os.path.join(_get_data_dir(), key_file)

def is_key_exists(key_file):
    return os.path.exists(os.path.join(_get_data_dir(), key_file))

def del_key_file(key_file):
    if is_key_exists(key_file):
        os.remove(os.path.join(_get_data_dir(), key_file))
    else:
        pass


# End of File