from typing import Tuple

from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

from src.utils import get_color_scheme


def get_user_resolution() -> Tuple[int, int]:
    # use this info to re-scale, so to avoid hardcoding
    user_w = QDesktopWidget().screenGeometry(-1).width()
    user_h = QDesktopWidget().screenGeometry(-1).height()
    return user_w, user_h


def open_disclaimer() -> None:
    # Hardcoding for now
    t = "<h2>DISCLAIMER</h2>\n"
    t += """
    Warship Girls Viewer (as "WGViewer") is not a representative and is not
    associated with Warship Girls (as "the game"), Warship Girls R (as "the game"),
    or Moefantasy 幻萌网络.
    <br><br>
    The copyright of the shipgirl art resources used in the
    WGViewer belong to Moefantasy.
    <br><br>
    WGViewer is intended for educational purposes only. Botting is in violation of
    the User Agreement of the game; prolonged usage of WGViewer's automation
    functions may result in your game account being banned. The developer of
    WGViewer takes no responsibility for repercussions related to the usage of
    WGViewer.
    <br><br>
    Although unlikely, users may sink ships and lose equipment when using WGViewer
    to conduct combat sorties. While WGViewer has been painstakingly designed to
    reduce chances of such occurrence, the developer of WGViewer does not take
    responsibility for any loss of ships and/or resources.
    """
    popup_msg(t, 'Terms and Conditions')


def popup_msg(text: str, title: str = None) -> None:
    msg = QMessageBox()
    msg.setStyleSheet(get_color_scheme())
    t = title if title is not None else "Info"
    msg.setWindowTitle(t)
    msg.setText(text)
    msg.exec_()


def open_url(url: str) -> None:
    QDesktopServices.openUrl(QUrl(url))


def quit_application() -> None:
    # TODO: in the future, save unfinished tasks
    QCoreApplication.exit()

# End of File
