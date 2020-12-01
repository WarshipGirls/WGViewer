# import json
import logging
import os
import zipfile

# import requests
import urllib.request
# from urllib.error import URLError
# from time import sleep

equip_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/E.zip"
ship_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/S.zip"
init_zip_url = "https://github.com/WarshipGirls/WGViewer/raw/master/zip/init.zip"
my_urls = [equip_zip_url, ship_zip_url, init_zip_url]

"""
def save_init_data():
    logging.info('Initializing data for first-time user... This may take 30+ seconds...')
    storage_dir = get_init_dir()
    res = [False]
    while not res[0]:
        try:
            res = _check_data_ver(storage_dir)
            if res[0]:
                pass
            else:
                res[0] = _save_all_attr(storage_dir, res[1])
        except (TimeoutError, requests.exceptions.ConnectionError):
            logging.error('Data initializing failed. Trying again...')
            sleep(5)

def _save_data_by_attr(storage_dir, data_dict, field):
    try:
        filename = field + '.json'
        p = os.path.join(storage_dir, filename)
        if os.path.exists(p):
            pass
        else:
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(data_dict[field], f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(e)
        return False
    return True


def _save_all_attr(storage_dir, data):
    res = True
    for k in data.keys():
        res &= _save_data_by_attr(storage_dir, data, k)
    return res


def _check_data_ver(storage_dir):
    # Note: since getting raw data takes 20+ seconds, use this method minimally
    # TODO: this is Chinese data; is there a link for English counterpart?
    url = 'http://login.jr.moefantasy.com/index/getInitConfigs'
    # url = 'http://loginios.jr.moefantasy.com/index/getInitConfigs'
    d = None
    try:
        d = requests.get(url).json()
    except (URLError, json.decoder.JSONDecodeError):
        logging.error('Server connection error. Please try again later.')
        return [False, d]

    path = os.path.join(storage_dir, 'DataVersion.json')
    if not os.path.exists(path):
        res = [False, d]
        logging.info('DataVersion file is missing. Updating now.')
    else:
        with open(path, encoding='utf-8') as f:
            x = json.load(f)
            if x == d['DataVersion']:
                res = [True, {}]
                logging.info('getInitConfigs data is already up-to-date.')
            else:
                res = [False, d]
                logging.info('getInitConfigs data is updating.')
    return res
"""


def _download(url: str) -> str:
    # download from Github
    l = url.rindex('/') + 1
    filename = url[l:]
    filepath = os.path.join(get_zip_dir(), filename)

    def _progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        progress = int((downloaded / total_size) * 100)
        logging.info("Download Progress", str(progress), "%")

    local_filename, _ = urllib.request.urlretrieve(url=url, filename=filepath, reporthook=_progress)
    return filename


def _download_all(urls) -> list:
    res = []
    for url in urls:
        logging.info(f'Downloading {url}')
        res.append(_download(url))
    return res


def _unzip_file(filename: str):
    # filename with extension
    path = os.path.join(get_zip_dir(), filename)
    if os.path.exists(path):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(get_zip_dir())
    else:
        logging.error('Filepath not exists: {}'.format(path))


def _unzip_all(filenames: list):
    for filename in filenames:
        _unzip_file(filename)


def init_resources():
    res = _download_all(my_urls)
    _unzip_all(res)


if __name__ == "__main__":
    try:
        from src.data.wgv_path import get_zip_dir
    except ModuleNotFoundError:
        from wgv_path import get_zip_dir
else:
    from .wgv_path import get_zip_dir

# End of File
