import logging

import urllib.request

from PyQt5.QtWidgets import QMessageBox
from packaging import version

from src.utils.general import get_app_version, open_url, _force_quit, popup_msg


class VersionCheck:
    def __init__(self, parent):
        self.latest_ver = None
        self.parent = parent

        try:
            self.check_version()
        except urllib.error.HTTPError as e:
            logging.error(e)

    def check_version(self) -> None:
        url = 'https://raw.githubusercontent.com/WarshipGirls/WGViewer/master/version'
        req = urllib.request.urlopen(url)
        if req.getcode() == 200:
            user_ver = version.parse(get_app_version())
            self.latest_ver = req.read().decode()
            latest_ver = version.parse(self.latest_ver)

            if user_ver == latest_ver:
                logging.info('LOGIN - User has latest version installed.')
                res = 0
            elif user_ver < latest_ver:
                res = self.detail_version_check(user_ver, latest_ver)
            elif user_ver > latest_ver:
                logging.error(f'LOGIN - Version check has unexpected outcome user: {user_ver}, cloud: {latest_ver}')
                res = -1
            else:
                logging.error(f'LOGIN - Version check has unexpected outcome user: {user_ver}, cloud: {latest_ver}')
                res = -1
        else:
            popup_msg('Latest app version check failed due to bad Internet connection.')
            res = 1

        if res == 0:
            logging.info('LOGIN - Version check succeed.')
        elif res == 1:
            logging.info('LOGIN - Version check succeed. User skips the latest download.')
        elif res == -1:
            popup_msg('Version check failed. Please re-download the application.', 'Info')
            _force_quit(0)
        else:
            pass

    def detail_version_check(self, user_ver: version.Version, latest_ver: version.Version) -> int:
        if user_ver.major < latest_ver.major:
            popup_msg(f'WGViewer v{self.latest_ver} is available. This is a mandatory major update', 'Major Update')
            res = True
        elif user_ver.minor < latest_ver.minor:
            res = self.is_update('Minor Update', 'a recommended')
        elif user_ver.micro < latest_ver.micro:
            res = self.is_update('Micro Update', 'an optional')
        else:
            logging.error(f'LOGIN - Version check has unexpected outcome user: {user_ver}, cloud: {latest_ver}')
            res = self.is_update('Update', 'an optional')
        if res is True:
            r = self.download_update()
        else:
            r = 1
        return r

    def is_update(self, title: str, body: str) -> bool:
        t = f'New WGViewer Available - {title}'
        b = f'WGViewer v{self.latest_ver} is available. This is {body} update.'
        b += "\nDo you wish to download the latest version?"
        reply = QMessageBox.question(self.parent, t, b, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # Lesson: Use `==` when comparing QMessageBox options
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    @staticmethod
    def download_update() -> int:
        # TODO long-term: auto start download?
        logging.info('LOGIN - Link to latest version of WGViewer')
        open_url('https://github.com/WarshipGirls/WGViewer/releases')
        return 0
