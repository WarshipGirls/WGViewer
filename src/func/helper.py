import hashlib
import time
import zlib

from .session import GameSession
from . import constants as constants


class Helper:
    """
    This Class is meant for game URL connections only
    """

    def __init__(self, sess=None):
        if sess is None:
            self.sess = GameSession()
        else:
            self.sess = sess

    @staticmethod
    def get_url_end(channel, now_time=str(int(round(time.time() * 1000)))):
        url_time = now_time
        # TODO: how to get the key in the first place? The encryption of URL part is the single point of failure of the app
        md5_raw = url_time + 'ade2688f1904e9fb8d2efdb61b5e398a'
        md5 = hashlib.md5(md5_raw.encode('utf-8')).hexdigest()
        url_end = f'&t={url_time}&e={md5}&version={constants.version}&channel={channel}&gz=1&market=3'
        return url_end

    def decompress_data(self, url, cookies, *data):
        if len(data) == 0:
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

# End of File
