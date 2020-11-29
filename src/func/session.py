import requests
import logging

from time import sleep


class Session:
    def __init__(self):
        self.session = requests.session()
        self.max_retry = 5
        self.sleep_time = 3

        self.accept_errors = (
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError
        )

    def new_session(self):
        self.session = requests.session()
        self.session.keep_alive = False

    def get(self, url, **kwargs):
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

    def post(self, url, data=None, json=None, **kwargs):
        for i in range(self.max_retry):
            try:
                r = self.session.post(url=url, data=data, json=json, **kwargs)
                r.close()
                return r
            except self.accept_errors as e:
                logging.warning(f"SESS - {e}")
                sleep(self.sleep_time)
                if i == 4:
                    raise


# End of File