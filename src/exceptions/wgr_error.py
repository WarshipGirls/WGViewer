import json
import os
import sys

from typing import NoReturn  # Differ than None; NoReturn for abnormally end a function

from PyQt5.QtCore import pyqtSignal
from src.utils import increase_sleep_interval


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


with open(get_data_path('assets/data/errorCode.json'), 'r', encoding='utf-8') as f:
    ERROR_JSON = json.load(f)

SIG_SPEED_TICKET = pyqtSignal()
SIG_SPEED_TICKET.connect(increase_sleep_interval)


class WarshipGirlsExceptions(Exception):
    def __init__(self, error_id, error_msg):
        super().__init__(error_id, error_msg)
        self.error_id = error_id
        self.error_msg = error_msg

    def __str__(self) -> str:
        return f"WGR-ERROR: {self.error_msg}"


def get_error(error_id: [str, int]) -> NoReturn:
    if str(error_id) in ERROR_JSON:
        if str(error_id) == "-1":
            SIG_SPEED_TICKET.emit()
        else:
            pass
        raise WarshipGirlsExceptions(error_id, ERROR_JSON[str(error_id)])
    else:
        raise WarshipGirlsExceptions(0, "UNKNOWN ERROR")

# End of File
