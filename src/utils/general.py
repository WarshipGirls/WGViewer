import datetime
import os
import qdarkstyle
import re
import time

from random import randint
from PyQt5.QtCore import QSettings

from src.data import get_qsettings_file
from src.func import qsettings_keys as QKEYS

_qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)


def clear_desc(text: str) -> str:
    # This garbage code (like ^C454545FF00000000) is probably due to cocoa?
    return re.sub(r'\^.+?00000000', '', text)


def get_app_version() -> str:
    return '0.2.1dev'


def get_color_scheme() -> str:
    if get_color_option() == "native":
        return ""
    else:
        _qsettings.setValue(QKEYS.STYLE, "qdarkstyle")
        return qdarkstyle.load_stylesheet(qt_api='pyqt5')


def get_color_option() -> str:
    return _qsettings.value(QKEYS.STYLE) if _qsettings.contains(QKEYS.STYLE) else "qdarkstyle"


def get_game_version() -> str:
    return '5.1.0'


def get_curr_time() -> str:
    return datetime.datetime.now().strftime('%H:%M:%S')


def get_unixtime() -> int:
    return int(time.time())


def get_today() -> str:
    return datetime.date.today().strftime('%Y-%m-%d')


def force_quit(code: int) -> None:
    os._exit(code)


def set_sleep(level: float = 1.0):
    # There must be some interval between Game API calls
    if _qsettings.contains(QKEYS.GAME_SPD_LO):
        lo = int(_qsettings.value(QKEYS.GAME_SPD_LO))
    else:
        lo = 5
    if _qsettings.contains(QKEYS.GAME_SPD_HI):
        hi = int(_qsettings.value(QKEYS.GAME_SPD_HI))
    else:
        hi = 10
    try:
        assert (lo < hi)
        time.sleep(randint(lo, hi) * level)
    except AssertionError:
        time.sleep(randint(5, 10) * level)


def ts_to_countdown(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds))


def ts_to_date(ts: int) -> str:
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# End of File
