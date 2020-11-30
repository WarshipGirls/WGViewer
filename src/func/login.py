import base64
import datetime
import hashlib
import hmac
import json
import logging
import random
import time
import urllib
import zlib

from . import constants as constants
from .helper_function import Helper


class GameLogin:
    """
    1st login: channel cookie version server_list
    2nd login: return nothing; init data
    """

    def __init__(self, game_version, game_channel, game_session, login_button):
        self.version = game_version
        self.channel = game_channel
        self.session = game_session
        self.login_button = login_button

        self.uid = None
        self.cookies = None
        self.login_server = ""
        self.key = constants.login_key
        self.portHead = ""
        self.hm_login_server = ""
        self.passport_headers = {
            "Accept-Encoding": "gzip",
            'User-Agent': 'okhttp/3.4.1',
            "Content-Type": "application/json; charset=UTF-8"
        }

        self.hlp = Helper(self.session)

    def first_login(self, username, pwd):
        logging.info("LOGIN - first server fetching...")
        url_version = f"http://version.jr.moefantasy.com/index/checkVer/{self.version}/{self.channel}/2&version={self.version}&channel={self.channel}&market=2"
        self.portHead = "881d3SlFucX5R5hE"
        # -------------------------------------------------------------------------------------------
        # Pull version Info
        response_version = self.session.get(url=url_version, headers=constants.header, timeout=10)
        response_version = json.loads(response_version.text)

        # Pull version number, login address
        # self.version = response_version["version"]["newVersionId"]
        self.login_server = response_version["loginServer"]
        self.hm_login_server = response_version["hmLoginServer"]

        # -------------------------------------------------------------------------------------------
        # For game log in
        server_data = self.login_usual(username=username, pwd=pwd)

        if not server_data:
            logging.error("LOGIN - First fetch failed")
            return False

        # self.defaultServer = int(server_data["defaultServer"])
        # self.server_list = server_data["serverList"]
        self.uid = server_data["userId"]

        logging.info("LOGIN - First fetch succeed!")
        return True

    def cheat_sess(self, host, link):
        # TODO the text is not get set in this file!
        self.login_button.setText(link)

        time.sleep(0.5)
        url_cheat = host + link + self.hlp.get_url_end(self.channel)
        self.session.get(url=url_cheat, headers=constants.header, cookies=self.cookies, timeout=10)

    def second_login(self, host):
        logging.info("LOGIN - second data fetching...")
        # Generate random device number
        now_time = str(int(round(time.time() * 1000)))
        random.seed(hashlib.md5(self.uid.encode('utf-8')).hexdigest())

        if self.channel == "100020":
            data_dict = constants.ios_data_dict
        elif self.channel == "100015":
            data_dict = constants.android_data_dict
        else:
            data_dict = {}
        data_dict["udid"] = str(random.randint(100000000000000, 999999999999999))
        data_dict["t"] = now_time
        data_dict["e"] = self.hlp.get_url_end(self.channel, now_time)
        random.seed()
        try:
            # Pull decisive data
            login_url_tmp = host + 'index/login/' + self.uid + '?&' + urllib.parse.urlencode(data_dict)
            self.session.get(url=login_url_tmp, headers=constants.header, cookies=self.cookies, timeout=10)

            # TODO, process following data
            # TODO, update to latest API
            self.cheat_sess(host, 'pevent/getPveData/')
            self.cheat_sess(host, 'shop/canBuy/1/')
            self.cheat_sess(host, 'live/getUserInfo')
            self.cheat_sess(host, 'live/getMusicList/')
            self.cheat_sess(host, 'bsea/getData/')
            self.cheat_sess(host, 'active/getUserData')
            self.cheat_sess(host, 'pve/getUserData/')
        except Exception:
            return False

        return True

    # Normal game log-in method
    def login_usual(self, username, pwd):
        url_login = self.hm_login_server + "1.0/get/login/@self"
        data = {
            "platform": "0",
            "appid": "0",
            "app_server_type": "0",
            "password": pwd,
            "username": username
        }

        self.refresh_headers(url_login)

        login_response = self.session.post(url=url_login, data=json.dumps(data).replace(" ", ""),
                                           headers=self.passport_headers, timeout=10)
        login_response = json.loads(login_response.text)

        if "error" in login_response and int(login_response["error"]) != 0:
            return False

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
        login_response = self.session.get(url=login_url, headers=constants.header, timeout=10)
        login_text = json.loads(zlib.decompress(login_response.content))

        self.cookies = login_response.cookies.get_dict()
        self.uid = str(login_text['userId'])
        return login_text

    def encryption(self, url, method):
        times = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

        data = str(method) + "\n" + times + "\n" + "/" + url.split("/", 3)[-1]
        mac = hmac.new(self.key.encode(), data.encode(), hashlib.sha1)
        data = mac.digest()
        return base64.b64encode(data).decode("utf-8"), times

    def refresh_headers(self, url):
        data, times = self.encryption(url=url, method="POST")
        self.passport_headers["Authorization"] = "HMS {}:".format(self.portHead) + data
        self.passport_headers["Date"] = times

    def get_cookies(self):
        return self.cookies

# End of File
