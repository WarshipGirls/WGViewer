import json
import os
import sys

from typing import NoReturn  # Differ than None; NoReturn for abnormally end a function

from src.utils import popup_msg


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


with open(get_data_path('assets/data/errorCode.json'), 'r', encoding='utf-8') as f:
    error_json = json.load(f)


class WarshipGirlsExceptions(Exception):
    def __init__(self, error_id, error_msg):
        super().__init__(error_id, error_msg)
        self.error_id = error_id
        self.error_msg = error_msg

    def __str__(self) -> str:
        return f"WGR-ERROR: {self.error_msg}"


def get_error(error_id: [str, int]) -> NoReturn:
    if str(error_id) in error_json:
        raise WarshipGirlsExceptions(error_id, error_json[str(error_id)])
    else:
        raise WarshipGirlsExceptions("UNKNOWN ERROR")

# End of File
