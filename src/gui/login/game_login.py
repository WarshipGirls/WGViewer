import base64
import datetime
import hashlib
import hmac
import json
import random
import time
import urllib
import zlib

from PyQt5.QtWidgets import QPushButton

from src.data import save_cookies
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from src.utils import get_app_version
from src.exceptions.wgr_error import get_error
from .helper import LoginHelper
from .session import LoginSession

logger = get_logger(QLOGS.LOGIN)

HEADER = {
    'Accept-Encoding': 'identity',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9.1.1; SAMSUNG-SM-G900A Build/LMY47X)'
}

ANDROID_DATA_DICT = {
    'client_version': get_app_version(),
    'phone_type': 'samsung note 9',
    'phone_version': '9.1.1',
    'ratio': '2960*1440',
    'service': 'CHINA MOBILE',
    'udid': '',
    'source': 'android',
    'affiliate': 'WIFI',
    't': '-1',
    'e': '-1',
    'gz': '1',
    'market': '2',
    'channel': '100015',
    'version': get_app_version()
}

IOS_DATA_DICT = {
    'client_version': get_app_version(),
    'phone_type': '',
    'phone_version': '13.7',
    'ratio': '2160*1620',
    'service': '',
    'udid': '',
    'source': 'ios',
    'affiliate': 'WIFI',
    't': '-1',
    'e': '-1',
    'gz': '1',
    'market': '2',
    'channel': '100020',
    'version': get_app_version()
}


class GameLogin:
    """
    1st login: channel cookie version server_list
    2nd login: return nothing; init data
    """

    def __init__(self, game_version: str, game_channel: str, game_session: LoginSession, login_button: QPushButton):
        self.version = game_version
        self.channel = game_channel
        self.session = game_session
        self.login_button = login_button

        self.server = ""
        self.uid = None
        self.cookies = None
        self.login_server = ""
        self.key = "kHPmWZ4zQBYP24ubmJ5wA4oz0d8EgIFe"
        self.portHead = "881d3SlFucX5R5hE"
        self.hm_login_server = ""
        self.passport_headers = {
            "Accept-Encoding": "gzip",
            'User-Agent': 'okhttp/3.4.1',
            "Content-Type": "application/json; charset=UTF-8"
        }

        self.hlp = LoginHelper(self.session)

    def first_login(self, username: str, password: str) -> bool:
        logger.info("first server fetching...")
        url_version = f"http://version.jr.moefantasy.com/index/checkVer/{self.version}/{self.channel}/2&version={self.version}&channel={self.channel}&market=2"
        # Pull version Info
        response_version = self.session.get(url=url_version, headers=HEADER, timeout=10)
        response_version = json.loads(response_version.text)

        if 'eid' in response_version:
            get_error(response_version['eid'])
            return False
        else:
            pass

        # Pull version number, login address
        # self.version = response_version["version"]["newVersionId"]
        self.login_server = response_version["loginServer"]
        self.hm_login_server = response_version["hmLoginServer"]

        # For game log in
        server_data = self.login_usual(username=username, password=password)
        if not server_data:
            return False

        self.uid = server_data["userId"]

        return True

    def cheat_sess(self, host: str, link: str) -> None:
        self.login_button.setText("Loading " + link)

        time.sleep(0.5)
        url_cheat = host + link + self.hlp.get_url_end(self.channel)
        self.session.get(url=url_cheat, headers=HEADER, cookies=self.cookies, timeout=10)

    def second_login(self, host: str) -> bool:
        logger.info("second data fetching...")
        # Generate random device number
        now_time = str(int(round(time.time() * 1000)))
        try:
            random.seed(hashlib.md5(self.uid.encode('utf-8')).hexdigest())
        except AttributeError:
            return False

        if self.channel == "100020":
            data_dict = IOS_DATA_DICT
        elif self.channel == "100015":
            data_dict = ANDROID_DATA_DICT
        else:
            data_dict = {}
        data_dict["udid"] = str(random.randint(100000000000000, 999999999999999))
        data_dict["t"] = now_time
        data_dict["e"] = self.hlp.get_url_end(self.channel, now_time)
        random.seed()
        self.server = host
        try:
            # Pull decisive data
            login_url_tmp = host + 'index/login/' + self.uid + '?&' + urllib.parse.urlencode(data_dict)
            self.session.get(url=login_url_tmp, headers=HEADER, cookies=self.cookies, timeout=10)

            # TODO: all of these are redundant
            self.cheat_sess(host, 'pevent/getPveData/')
            # self.cheat_sess(host, 'shop/canBuy/1/')
            self.cheat_sess(host, 'live/getUserInfo')
            # self.cheat_sess(host, 'live/getMusicList/')
            self.cheat_sess(host, 'bsea/getData/')
            self.cheat_sess(host, 'active/getUserData')
            self.cheat_sess(host, 'pve/getUserData/')
        except Exception:
            return False

        return True

    # Normal game log-in method
    def login_usual(self, username: str, password: str) -> dict:
        url_login = self.hm_login_server + "1.0/get/login/@self"
        data = {
            "platform": "0",
            "appid": "0",
            "app_server_type": "0",
            "password": password,
            "username": username
        }

        self.refresh_headers(url_login)
        login_response = self.session.post(url=url_login, data=json.dumps(data).replace(" ", ""), headers=self.passport_headers, timeout=10)
        login_response = json.loads(login_response.text)

        if "error" in login_response and int(login_response["error"]) != 0:
            return {}

        tokens = ""
        if "access_token" in login_response:
            tokens = login_response["access_token"]
        if "token" in login_response:
            tokens = login_response["token"]

        url_init = self.hm_login_server + "1.0/get/initConfig/@self"
        self.refresh_headers(url_init)
        self.session.post(url=url_init, data="{}", headers=self.passport_headers, timeout=10)
        time.sleep(1)

        # Validate token
        while True:
            url_info = self.hm_login_server + "1.0/get/userInfo/@self"
            login_data = json.dumps({"access_token": tokens})

            self.refresh_headers(url_info)
            user_info = self.session.post(url=url_info, data=login_data, headers=self.passport_headers, timeout=10).text
            user_info = json.loads(user_info)
            if "error" in user_info and user_info["error"] != 0:
                tokens = ""
                continue
            else:
                break

        login_url = self.login_server + "index/hmLogin/" + tokens + self.hlp.get_url_end(self.channel)
        login_response = self.session.get(url=login_url, headers=HEADER, timeout=10)
        try:
            login_text = json.loads(zlib.decompress(login_response.content))
        except zlib.error as e:
            logger.error(e)    # incorrect header check
            return {}

        self.cookies = login_response.cookies.get_dict()
        self.uid = str(login_text['userId'])
        return login_text

    def refresh_headers(self, url: str) -> None:
        times = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        data = "POST\n" + times + "\n" + "/" + url.split("/", 3)[-1]
        # encryption
        mac = hmac.new(self.key.encode(), data.encode(), hashlib.sha1)
        data = mac.digest()
        data = base64.b64encode(data).decode("utf-8")

        self.passport_headers["Authorization"] = f"HMS {self.portHead}:{data}" 
        self.passport_headers["Date"] = times

    def get_cookies(self) -> dict:
        output = {'server': self.server, 'channel': self.channel, 'cookies': self.cookies}
        save_cookies(output)
        return output

# End of File
