import os
import re

from datetime import datetime, timedelta
from random import randint
from time import sleep


def clear_desc(text: str) -> str:
    # This garbage code (like ^C454545FF00000000) is probably due to cocoa?
    return re.sub(r'\^.+?00000000', '', text)


def get_app_version() -> str:
    return '0.1.1dev'


def get_curr_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def get_game_version() -> str:
    return '5.1.0'


def force_quit(code: int) -> None:
    os._exit(code)


def ts_to_countdown(seconds: int) -> str:
    return str(timedelta(seconds=seconds))


def ts_to_date(ts: int) -> str:
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def set_sleep(level: float = 1.0):
    # There must be some interval between Game API calls
    # TODO: make this global settings
    sleep(randint(5, 10) * level)

# End of File
