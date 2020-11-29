import json
import logging
import os
import requests
import shutil
import urllib

from time import sleep

# TODO: maybe add init.zip to cloud, and use script to auto update it.
# https://drive.google.com/file/d/19L7UB00C1oSqYEshP3gRiraTTnzlH19b/view?usp=sharing

# ================================
# Exports
# ================================

def save_init_data():
    '''
    Updating data to the latest version
    '''
    logging.info('Initializing data for first-time user... This may take 30+ seconds...')
    storage_dir = get_init_dir()
    res = [False]
    while not res[0]:
        try:
            res = _check_data_ver(storage_dir)
            if res[0] == True:
                pass
            else:
                res[0] = _save_all_attr(storage_dir, res[1])
        except (TimeoutError, requests.exceptions.ConnectionError) as e:
            logging.error('Data initializing failed. Trying again...')
            sleep(5)


# ================================
# Not Exports
# ================================


def _save_data_by_attr(storage_dir, data_dict, field):
    try:
        filename = field + '.json'
        p = os.path.join(storage_dir, filename)
        if os.path.exists(p):
            pass
        else:
            with open(p, 'w', encoding='utf-8') as fout:
                json.dump(data_dict[field], fout, ensure_ascii=False, indent=4)
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
    try:
        d = requests.get(url).json()
    except (urllib.error.URLError, json.decoder.JSONDecodeError) as e:
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


# End of File