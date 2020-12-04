import json
import os
import sys
from typing import NoReturn


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class WarshipGirlsException(Exception):
    def __init__(self, message):
        super().__init__(message)


with open(get_data_path('assets/data/errorCode.json'), 'r', encoding='utf-8') as f:
    error_json = json.load(f)


def get_error(error_code: str) -> NoReturn:
    if error_code in error_json:
        raise WarshipGirlsException(error_json[error_code])
    else:
        raise WarshipGirlsException("UNKNOWN ERROR")

# End of File
