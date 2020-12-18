from typing import Union

import requests
import logging

from time import sleep

from PyQt5.QtCore import QSettings
from requests import Response

from src.data import get_qsettings_file
from src.func import qsettings_keys as QKEYS


class LoginSession:
    def __init__(self):
        self.session = requests.sessions.Session()
        self.qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
        if self.qsettings.contains(QKEYS.CONN_SESS_RTY) is True:
            self.max_retry = self.qsettings.value(QKEYS.CONN_SESS_RTY, type=int)
        else:
            self.max_retry = 5
        if self.qsettings.contains(QKEYS.CONN_SESS_SLP) is True:
            self.sleep_time = self.qsettings.value(QKEYS.CONN_SESS_SLP, type=int)
        else:
            self.sleep_time = 3

        self.accept_errors = (
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError
        )

    def new_session(self) -> None:
        self.session = requests.sessions.Session()
        self.session.keep_alive = False

    def get(self, url: str, **kwargs) -> Union[Response, None]:
        for i in range(self.max_retry):
            try:
                r = self.session.get(url=url, **kwargs)
                self.wait_until_success(r)
                r.close()
                return r
            except self.accept_errors as e:
                logging.warning(f"SESS - {e}")
                sleep(self.sleep_time)
                if i == 4:
                    raise

    def post(self, url: str, data=None, json=None, **kwargs) -> Union[Response, None]:
        for i in range(self.max_retry):
            try:
                r = self.session.post(url=url, data=data, json=json, **kwargs)
                self.wait_until_success(r)
                r.close()
                return r
            except self.accept_errors as e:
                logging.warning(f"SESS - {e}")
                sleep(self.sleep_time)
                if i == 4:
                    raise

    @staticmethod
    def wait_until_success(response: Response, timeout: float = 3.0, timewait: float = 1.0) -> None:
        # for session.get() / post()
        logging.debug("session - waiting for aborted")
        timer = 0
        while response.status_code != 200:
            logging.debug(f"session - waiting for aborted {timer}")
            sleep(timewait)
            timer += timewait
            if timer > timeout:
                break
            if response.status_code == 200:
                break

# End of File
