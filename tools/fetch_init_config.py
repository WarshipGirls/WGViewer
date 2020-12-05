import json
import logging
import os

from time import sleep
from urllib.error import URLError

import requests


# TODO auto zip

def save_init_data():
    logging.info('Initializing data for first-time user... This may take 30+ seconds...')
    storage_dir = "./"
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


save_init_data()

# End of File
