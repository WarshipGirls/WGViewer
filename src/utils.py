import re
from datetime import datetime, timedelta

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox
from src import data as wgr_data


def clear_desc(text: str) -> str:
    # This garbage code (like ^C454545FF00000000) is probably due to cocoa?
    return re.sub(r'\^.+?00000000', '', text)


def ts_to_date(ts: int):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def ts_to_countdown(seconds: int) -> str:
    return str(timedelta(seconds=seconds))


def popup_msg(text: str):
    msg = QMessageBox()
    msg.setStyleSheet(wgr_data.get_color_scheme())
    msg.setWindowTitle("Info")
    msg.setText(text)
    msg.exec_()


def open_url(self, url: str):
    QDesktopServices.openUrl(QUrl(url))

# End of File
