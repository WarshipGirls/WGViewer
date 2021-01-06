import datetime
import logging
import os
import qdarkstyle
import re
import time

from random import randint
from threading import Event
from typing import List
from PyQt5.QtCore import QSettings, pyqtSlot

from src.data import get_qsettings_file
from src.func import qsettings_keys as QKEYS
from src.func.worker import Worker

_qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
_sleep_event = Event()


def clear_desc(text: str) -> str:
    # This garbage code (like ^C454545FF00000000) is probably due to cocoa?
    return re.sub(r'\^.+?00000000', '', text)


def get_app_version() -> str:
    return '0.2.3.1dev'


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


def force_quit(code: int) -> None:
    os._exit(code)


def welcome_console_message() -> List[str]:
    x = ['██╗    ██╗ ██████╗ ██╗   ██╗██╗███████╗██╗    ██╗███████╗██████╗ ',
         '██║    ██║██╔════╝ ██║   ██║██║██╔════╝██║    ██║██╔════╝██╔══██╗',
         '██║ █╗ ██║██║  ███╗██║   ██║██║█████╗  ██║ █╗ ██║█████╗  ██████╔╝',
         '██║███╗██║██║   ██║╚██╗ ██╔╝██║██╔══╝  ██║███╗██║██╔══╝  ██╔══██╗',
         '╚███╔███╔╝╚██████╔╝ ╚████╔╝ ██║███████╗╚███╔███╔╝███████╗██║  ██║',
         ' ╚══╝╚══╝  ╚═════╝   ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝']
    return x


# ================================
# Timer
# ================================


def get_curr_time() -> str:
    return datetime.datetime.now().strftime('%H:%M:%S')


def get_today() -> str:
    return datetime.date.today().strftime('%Y-%m-%d')


def get_unixtime() -> int:
    return int(time.time())


def ts_to_countdown(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds))


def ts_to_date(ts: int) -> str:
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


# ================================
# Sleep Event
# ================================

def _increase_sleep_interval() -> None:
    lo = _qsettings.value(QKEYS.GAME_SPD_LO, type=int)
    hi = _qsettings.value(QKEYS.GAME_SPD_HI, type=int)
    _qsettings.setValue(QKEYS.GAME_SPD_LO, lo + 2)
    _qsettings.setValue(QKEYS.GAME_SPD_HI, hi + 2)


_worker = Worker(_increase_sleep_interval, ())
_worker.terminate()


@pyqtSlot()
def increase_sleep_interval() -> None:
    logging.debug('!! received speed ticket !!')
    _worker.start()


def reset_sleep_event() -> None:
    _sleep_event.clear()


def stop_sleep_event() -> None:
    # This is meant to interrupt the sleep event from outside,
    _sleep_event.set()


def set_sleep(level: float = 1.0):
    # There must be some interval between Game API calls
    if _qsettings.contains(QKEYS.GAME_SPD_LO):
        lo = _qsettings.value(QKEYS.GAME_SPD_LO, type=int)
    else:
        lo = 5
        _qsettings.setValue(QKEYS.GAME_SPD_LO, lo)
    if _qsettings.contains(QKEYS.GAME_SPD_HI):
        hi = _qsettings.value(QKEYS.GAME_SPD_HI, type=int)
    else:
        hi = 10
        _qsettings.setValue(QKEYS.GAME_SPD_HI, hi)

    if lo >= hi:
        hi += lo
        _qsettings.setValue(QKEYS.GAME_SPD_HI, hi)
    else:
        pass
    sleep_time = randint(lo, hi) * level
    _sleep_event.wait(sleep_time)

# End of File
