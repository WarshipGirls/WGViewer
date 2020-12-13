from typing import Union

import requests
import logging

from time import sleep

from requests import Response


class LoginSession:
    def __init__(self):
        self.session = requests.sessions.Session()
        self.max_retry = 5
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
    def wait_until_success(response: Response, timeout: float = 2.0, timewait: float = 0.5) -> None:
        # for session.get() / post()
        timer = 0
        while response.status_code == 204:
            sleep(timewait)
            timer += timewait
            if timer > timeout:
                break
            if response.status_code == 200:
                break

# End of File
