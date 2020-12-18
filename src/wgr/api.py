import json
import zlib

from ast import literal_eval
from socket import timeout

from PyQt5.QtCore import QSettings
from requests import exceptions
from requests.utils import cookiejar_from_dict
from time import sleep
from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.error import URLError
from http.client import HTTPResponse

from src.data import get_qsettings_file
from src.func import qsettings_keys as QKEYS
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from src.gui.login.helper import LoginHelper

logger = get_logger(QLOGS.API)


class WGR_API:
    """
    Warship Girls (R) - API
    """

    def __init__(self, cookies: dict):
        self.server = cookies['server']
        self.channel = cookies['channel']
        self.cookies = cookies['cookies']

        self.hlp = LoginHelper()
        qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
        if qsettings.contains(QKEYS.CONN_API_RTY) is True:
            self.max_retry = qsettings.value(QKEYS.CONN_API_RTY, type=int)
        else:
            self.max_retry = 5
        if qsettings.contains(QKEYS.CONN_API_SLP) is True:
            self.sleep_time = qsettings.value(QKEYS.CONN_API_SLP, type=int)
        else:
            self.sleep_time = 3

    def _api_call(self, link: str) -> dict:
        # This uses requests.sessions.Session().get() / post()
        data = None
        url = self.server + link + self.hlp.get_url_end(self.channel)
        res = False
        tries = 0
        while not res:
            try:
                raw_data = self.hlp.session_get(url=url, cookies=self.cookies)
                data = json.loads(raw_data)
                res = True
            except (TimeoutError, exceptions.ReadTimeout) as e:
                logger.error(e)
                logger.warning('Trying reconnecting...')
                sleep(self.sleep_time)

            tries += 1
            if tries >= self.max_retry:
                logger.warning(f"Failed to connect to {link} after {self.max_retry} reconnections. Please try again later.")
                break
            else:
                pass
        return data

    def _api_urlopen(self, link: str) -> dict:
        # TODO: use this minimally! Currently the returned data is unreadable
        # This uses urllib.request.urlopen
        data = None
        url = self.server + link + self.hlp.get_url_end(self.channel)
        res = False
        tries = 0

        cj = cookiejar_from_dict(self.cookies)
        opener = build_opener(HTTPCookieProcessor(cj))
        _req = Request(url=url)
        # TODO hard-coding
        _req.add_header(key='Accept-Encoding', val='identity')
        _req.add_header(key='Connection', val='Keep-Alive')
        _req.add_header(key='User-Agent', val='Dalvik/2.1.0 (Linux; U; Android 9.1.1; SAMSUNG-SM-G900A Build/LMY47X)')
        while not res:
            try:
                # raw_data = opener.open(_req, timeout=10).read()
                response = opener.open(_req, timeout=10)
                self.wait_until_success(response)
                raw_data = response.read()
                try:
                    byte_data = zlib.decompress(raw_data)
                    data = literal_eval(byte_data.decode('ascii'))  # encoding type determined by chardet
                except zlib.error:
                    data = {}
                res = True
            except (TimeoutError, URLError, timeout) as e:
                logger.error(e)
                logger.warning('urlopen trying reconnecting...')
                sleep(self.sleep_time)

            tries += 1
            if tries >= self.max_retry:
                logger.warning(f"Failed to connect to {link} after {self.max_retry} reconnections. Please try again later.")
                break
            else:
                pass
        return data

    @staticmethod
    def wait_until_success(response: HTTPResponse, _timeout: float = 3.0, _timewait: float = 1.0) -> None:
        # for urlopen
        logger.debug("urlopen - waiting for aborted")
        timer = 0
        while response.status != 200:
            logger.debug(f"urlopen - waiting for aborted {timer}")
            sleep(_timewait)
            timer += _timewait
            if timer > _timeout:
                break
            if response.status == 200:
                break

    @staticmethod
    def _int_list_to_str(int_list: list) -> str:
        res = str(int_list).replace(' ', '')
        return res

    def active_getUserData(self):
        link = 'active/getUserData'
        return self._api_call(link)

    def bsea_getData(self):
        link = 'bsea/getData'
        return self._api_call(link)

    def getLoginAward(self):
        # link = 'active/getLoginAward/c3ecc6250c89e88d83832e3395efb973/'
        link = 'active/getLoginAward//'
        return self._api_call(link)

    def getShipList(self):
        link = 'api/getShipList'
        return self._api_call(link)

    def initGame(self):
        link = 'api/initGame?&crazy=1'
        return self._api_call(link)

    def live_getUserInfo(self):
        link = 'live/getUserInfo'
        return self._api_call(link)

    def pevent_getPveData(self):
        link = 'pevent/getPveData'
        return self._api_call(link)

    def rank_getData(self):
        link = 'rank/getData/'
        return self._api_call(link)

# End of File
