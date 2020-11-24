#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import json
import shutil
import urllib
import logging
import platform
import requests

from pathlib import Path


# ================================
# getInitConfigs related
# ================================


def get_storage_dir():
    # TODO: unix not tested
    # TODO: mac not tested
    plt = platform.system()
    _dir = ''
    if plt == "Windows":
        _dir = os.getenv('LOCALAPPDATA')
    elif plt == "Linux":
        _dir = os.path.join(str(Path.home()), '.config')
    elif plt == "Darwin":
        _dir = os.path.join(str(Path.home()), 'Library', 'Application Support')
    else:
        _dir = str(Path.home())
    return os.path.join(_dir, 'WarshipGirlsViewer')

def save_data_by_attr(storage_dir, data_dict, field):
    filename = field + '.json'
    p = os.path.join(storage_dir, filename)
    if os.path.exists(p):
        pass
    else:
        with open(p, 'w', encoding='utf-8') as fout:
            json.dump(data_dict[field], fout, ensure_ascii=False, indent=4)

def check_data_ver(storage_dir):
    # Note: since getting raw data takes 20+ seconds, use this method minimally
    url = 'http://login.jr.moefantasy.com/index/getInitConfigs'
    try:
        d = requests.get(url).json()
    except (urllib.error.URLError, json.decoder.JSONDecodeError) as e:
        logging.error('Server connection error. Please try again later.')
        logging.error(e)

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

def save_init_data():
    '''
    Updating data to the latest version
    '''
    # TODO: following need to be executed once for new user.
    storage_dir = os.path.join(get_storage_dir(), 'init')
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    else:
        pass

    res = check_data_ver(storage_dir)
    if res[0] == True:
        pass
    else:
        data = res[1]
        for k in data.keys():
            save_data_by_attr(storage_dir, data, k)


# ================================
# General
# ================================


def _clear_cache():
    _dir = get_storage_dir()
    for filename in os.listdir(_dir):
        file_path = os.path.join(_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error('Failed to delete %s. Reason: %s' % (file_path, e))


# ================================
# Temporary
# ================================


def map_equip(equipable_type):
    with open('shipEquipmnt.json', encoding='utf-8') as f1:
        x = json.load(f1)

    type_to_id = {}
    for e in x:
        if e['type'] in type_to_id:
            type_to_id[e['type']].append(e['cid'])
        else:
            type_to_id[e['type']] = []
            type_to_id[e['type']].append(e['cid'])

    # TODO: this is temp, get these from somewhere else
    with open('../example_json/api_initgame_mainaccount.json', encoding='utf-8') as f2:
        user_equips = json.load(f2)['equipmentVo']

    # loop thru equipable_type
    for t in equipable_type:
        # in each type, loop thru all equips
        for e in type_to_id[t]:
            # check the amount user owns in user_equips
            try:
                user_e = next((i for i in user_equips if i['equipmentCid'] == e))
            except StopIteration:
                continue
            if user_e['num'] == 0:
                continue
            else:
                print(user_e)

def type_equip_map(cid):
    with open('shipCard.json', encoding='utf-8') as f:
        x = json.load(f)

    ship = next((i for i in x if i['cid'] == cid))
    return ship['equipmentType']

# End of File