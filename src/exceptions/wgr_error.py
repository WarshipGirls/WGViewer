import json
import os
import sys

from typing import NoReturn  # Differ than None; NoReturn for abnormally end a function

from PyQt5.QtCore import pyqtSignal, QObject
from src.utils import increase_sleep_interval, popup_msg


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


with open(get_data_path('assets/data/errorCode.json'), 'r', encoding='utf-8') as f:
    ERROR_JSON = json.load(f)


class SpeedTicket(QObject):
    sig_speed_ticket = pyqtSignal()

    def __init__(self):
        # Only QObject can use pyqtSignal/pyqtSlot
        super(SpeedTicket, self).__init__()
        self.sig_speed_ticket.connect(increase_sleep_interval)

    def emit(self):
        self.sig_speed_ticket.emit()


class WarshipGirlsExceptions(Exception):
    def __init__(self, error_id, error_msg):
        super().__init__(error_id, error_msg)
        self.error_id = str(error_id)
        self.error_msg = error_msg

    def __str__(self) -> str:
        if self.error_id == "-1":  # Too fast
            s = SpeedTicket()
            s.emit()
        # elif self.error_id == "-9999":  # game server under maintenance
        # TODO: this lead to weird behavior
        #     popup_msg(self.error_msg)
        #     quit_application()
        else:
            pass
        return f"WGR-ERROR: {self.error_msg}"


def get_error(error_id: [str, int]) -> NoReturn:
    if str(error_id) in ERROR_JSON:
        raise WarshipGirlsExceptions(error_id, ERROR_JSON[str(error_id)])
    else:
        raise WarshipGirlsExceptions(0, "UNKNOWN ERROR")


def get_error_text(error_id: [str, int]) -> str:
    if str(error_id) in ERROR_JSON:
        res = ERROR_JSON[str(error_id)]
    else:
        res = "UNKNOWN ERROR"
    return res

# End of File
