import urllib.request

from PyQt5.QtWidgets import QMessageBox, QWidget
from packaging import version

from src import utils as wgv_utils
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from src.func.worker import CallbackWorker
from src.gui.custom_widgets import QtWaitingSpinner

logger = get_logger(QLOGS.LOGIN)


class WGViewerVersionCheck:
    def __init__(self):
        self.latest_ver = None
        self.is_check_finished = False
        self.loading_screen = QtWaitingSpinner(self)
        self.bee = CallbackWorker(self.fetch_version, (), self.fetch_finished)
        self.bee.terminate()
        try:
            self.loading_screen.start()
            self.bee.start()
        except urllib.error.HTTPError as e:
            logger.error(e)

    def fetch_finished(self, res: bool) -> None:
        self.loading_screen.stop()
        self.is_check_finished = True
        if res is True:
            user_ver = version.parse(wgv_utils.get_app_version())
            latest_ver = version.parse(self.latest_ver)
            if user_ver == latest_ver:
                logger.debug('User has latest version installed.')
                res = 0
            elif user_ver < latest_ver:
                res = self.detail_version_check(user_ver, latest_ver)
            elif user_ver > latest_ver:
                logger.error(f'Version check has unexpected outcome user: {user_ver}, cloud: {latest_ver}')
                res = -1
            else:
                logger.error(f'Version check has unexpected outcome user: {user_ver}, cloud: {latest_ver}')
                res = -1
        else:
            wgv_utils.popup_msg('Latest app version check failed due to bad Internet connection.')
            res = 1

        if res == 0:
            logger.debug('Version check succeed.')
        elif res == 1:
            logger.debug('Version check succeed. User skips the latest download.')
        elif res == -1:
            wgv_utils.popup_msg('Version check failed. Please re-download the application.', 'Info')
            wgv_utils.force_quit(0)
        else:
            pass

    def fetch_version(self) -> bool:
        url = 'https://raw.githubusercontent.com/WarshipGirls/WGViewer/master/version'
        req = urllib.request.urlopen(url)
        if req.getcode() == 200:
            self.latest_ver = req.read().decode()
            res = True
        else:
            res = False
        return res

    def detail_version_check(self, user_ver: version.Version, latest_ver: version.Version) -> int:
        if user_ver.major < latest_ver.major:
            wgv_utils.popup_msg(f'WGViewer v{self.latest_ver} is available. This is a mandatory major update', 'Major Update')
            res = True
        elif user_ver.minor < latest_ver.minor:
            res = self.is_update('Minor Update', 'a recommended')
        elif user_ver.micro < latest_ver.micro:
            res = self.is_update('Micro Update', 'an optional')
        else:
            logger.error(f'Version check has unexpected outcome user: {user_ver}, cloud: {latest_ver}')
            res = self.is_update('Update', 'an optional')

        if res is True:
            self.download_update()
            r = 0
        else:
            r = 1
        return r

    def is_update(self, title: str, body: str) -> bool:
        t = f'New WGViewer Available - {title}'
        b = f'WGViewer v{self.latest_ver} is available. This is {body} update.'
        b += "\nDo you wish to download the latest version?"
        reply = QMessageBox.question(QWidget(), t, b, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # Lesson: Use `==` when comparing QMessageBox options
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    @staticmethod
    def download_update() -> None:
        # TODO long-term: auto start download?
        wgv_utils.open_url('https://github.com/WarshipGirls/WGViewer/releases')

# End of File
