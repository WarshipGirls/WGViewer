import hashlib
import re
import time
import zlib

from datetime import datetime, timedelta

from .session import Session
from . import constants as constants


class Helper:
    def __init__(self, sess=None):
        if sess is None:
            self.sess = Session()
        else:
            self.sess = sess
        # self.sess = sess or Session()

    @staticmethod
    def get_url_end(channel, now_time=str(int(round(time.time() * 1000)))):
        url_time = now_time
        md5_raw = url_time + 'ade2688f1904e9fb8d2efdb61b5e398a'
        md5 = hashlib.md5(md5_raw.encode('utf-8')).hexdigest()
        url_end = '&t={time}&e={key}&version={version}&channel={channel}&gz=1&market=3'
        url_end_dict = {'time': url_time, 'key': md5, 'channel': channel, 'version': constants.version}
        url_end = url_end.format(**url_end_dict)
        return url_end

    def decompress_data(self, url, cookies, *data):
        if len(data) is 0:
            content = self.sess.get(url=url, headers=constants.header, cookies=cookies, timeout=10).content
        else:
            h = constants.header
            # https://stackoverflow.com/questions/4007969/application-x-www-form-urlencoded-or-multipart-form-data
            h["Content-Type"] = "application/x-www-form-urlencoded"
            content = self.sess.post(url=url, data=str(data[0]), headers=h, cookies=cookies, timeout=10).content
        try:
            data = zlib.decompress(content)
        except zlib.error:
            data = content
        return data

    @staticmethod
    def str_arg(**arg):
        new_arg = {}
        for index, key in arg.items():
            new_arg[index] = str(key)
        return new_arg

    @staticmethod
    def ts_to_date(ts: int):
        return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def ts_to_countdown(seconds: int):
        return str(timedelta(seconds=seconds))

    @staticmethod
    def clear_desc(input: str) -> str:
        # This garbage code (like ^C454545FF00000000) is probably due to cocoa?
        return re.sub(r'\^.+?00000000', '', input)

# End of File
