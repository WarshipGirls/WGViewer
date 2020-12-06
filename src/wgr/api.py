import json
import logging


from requests import exceptions
from requests.utils import cookiejar_from_dict
from time import sleep
from urllib.request import Request, urlopen, build_opener, HTTPCookieProcessor
from urllib.error import URLError

from src.func.helper import Helper


class WGR_API:
    """
    Warship Girls (R) - API
    """

    def __init__(self, cookies: dict):
        self.server = cookies['server']
        self.channel = cookies['channel']
        self.cookies = cookies['cookies']

        self.hlp = Helper()
        self.max_retry = 10
        self.sleep_time = 5

    def _api_call(self, link: str) -> object:
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
                logging.error(e)
                logging.warning('Trying reconnecting...')
                sleep(self.sleep_time)
            tries += 1
            if tries >= self.max_retry:
                logging.warning(f"Failed to connect to {link} after {self.max_retry} reconnections. Please try again later.")
                break
            else:
                pass
        return data

    def _api_urlopen(self, link: str) -> object:
        # This uses urllib.request.urlopen
        data = None
        url = self.server + link + self.hlp.get_url_end(self.channel)
        res = False
        tries = 0
        print('--------------------------------')
        print(url)
        print('--------------------------------')

        cj = cookiejar_from_dict(self.cookies)
        opener = build_opener(HTTPCookieProcessor(cj))

        _req = Request(url=url)
        _req.add_header(key='Accept-Encoding', val='identity')
        _req.add_header(key='Connection', val='Keep-Alive')
        _req.add_header(key='User-Agent', val='Dalvik/2.1.0 (Linux; U; Android 9.1.1; SAMSUNG-SM-G900A Build/LMY47X)')
        while not res:
            try:
                data = opener.open(_req, timeout=10).read()
                res = True
            except (TimeoutError, URLError) as e:
                logging.error(e)
                logging.warning('urlopen trying reconnecting...')

            tries += 1
            sleep(self.sleep_time)

            if tries >= self.max_retry:
                logging.warning(f"Failed to connect to {link} after {self.max_retry} reconnections. Please try again later.")
                break
            else:
                pass
        return data

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
