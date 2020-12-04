import json
import os
import sys


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class WGR_ERROR:
    def __init__(self):
        with open(get_data_path('assets/data/errorCode.json'), 'r', encoding='utf-8') as f:
            self.error_json = json.load(f)

    def get_info(self, error_code: str) -> str:
        if error_code in self.error_json:
            return self.error_json[error_code]
        else:
            return "UNKNOWN ERROR"

# End of File
