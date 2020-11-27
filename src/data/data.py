#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import logging
import os
import platform
import qdarkstyle
import requests
import shutil
import urllib

from PyQt5.QtCore import QSettings

from pathlib import Path
from time import sleep


# ================================
# General
# ================================


def _get_data_dir():
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

def _clear_dir(_dir):
    for filename in os.listdir(_dir):
        file_path = os.path.join(_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error('Failed to delete %s. Reason: %s' % (file_path, e))

def get_init_dir():
    p = os.path.join(_get_data_dir(), 'init')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p

def get_user_dir():
    p = os.path.join(_get_data_dir(), 'user')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p

def get_temp_dir():
    p = os.path.join(_get_data_dir(), 'temp')
    if not os.path.exists(p):
        os.makedirs(p)
    else:
        pass
    return p

def find_index(lst, key, value):
    '''
    Given a list of dict, find index by key-value pair.
    '''
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def find_all_indices(lst, key, value):
    res = []
    for i, dic in enumerate(lst):
        if dic[key] == value:
            res.append(i)
    return res

def get_color_scheme():
    qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
    s = qsettings.value("style") if qsettings.contains("style") else "qdarkstyle"
    if s == "native":
        return ""
    else:
        qsettings.setValue("style", "qdarkstyle")
        return qdarkstyle.load_stylesheet(qt_api='pyqt5')


# ================================
# QSettings
# ================================


def get_qsettings_file():
    return os.path.join(_get_data_dir(), 'wgviewer.ini')

def get_key_path(key_file):
    return os.path.join(_get_data_dir(), key_file)

def is_key_exists(key_file):
    return os.path.exists(os.path.join(_get_data_dir(), key_file))

def _del_key_file(key_file):
    if is_key_exists(key_file):
        os.remove(os.path.join(_get_data_dir(), key_file))
    else:
        pass


# ================================
# getInitConfigs
# ================================


def save_data_by_attr(storage_dir, data_dict, field):
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

def save_all_attr(storage_dir, data):
    res = True
    for k in data.keys():
        res &= save_data_by_attr(storage_dir, data, k)
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
                res[0] = save_all_attr(storage_dir, res[1])
        except (TimeoutError, requests.exceptions.ConnectionError) as e:
            logging.error('Data initializing failed. Trying again...')
            sleep(5)


# ================================
# Equipment
# shipEquipmnt.json contains the equipment you own;
# the `num` excludes those on ship
# ================================


def process_one_equip(equip):
    res = {}
    res['title'] = equip['title']
    res['desc'] = equip['desc']
    for key in equip.keys():
        if isinstance(equip[key], int):
            res[key] = equip[key]
        else:
            pass
    garbage = ['type', 'picId', 'cid', 'boreType', 'handbookType',
               'specialEffect', 'equipIndex', 'aluminiumUse', 'airDefRate']
    for g in garbage:
        try:
            res.pop(g)
        except KeyError:
            pass
    return res

""" Following implementation is not used because MF's bug
def _type_to_equips(equipable_types):
    '''
    Based on a ship equipable types, return all user owned equipment. 
    '''
    # 2. get all equipment id in shipEquipmnt (yes, no 'e')
    equip_path = os.path.join(get_init_dir(), 'shipEquipmnt.json')
    with open(equip_path, encoding='utf-8') as f1:
        all_equips = json.load(f1)

    type_to_id = {}
    id_to_data = {}
    for e in all_equips:
        if e['type'] in type_to_id:
            pass
        else:
            type_to_id[e['type']] = []
        type_to_id[e['type']].append(e['cid'])
        id_to_data[e['cid']] = process_one_equip(e)

    print(type_to_id)

    user_equip_path = os.path.join(get_user_dir(), 'equipmentVo.json')
    with open(user_equip_path, encoding='utf-8') as f2:
        user_equips = json.load(f2)

    # 3. get all user-owned equipment by equipment id
    res = []
    for t in equipable_types:
        for e in type_to_id[t]:
            try:
                user_e = next((i for i in user_equips if i['equipmentCid'] == e))
                user_e.pop('uid')
            except StopIteration:
                continue
            if user_e['num'] == 0:
                continue
            else:
                # can't pop `equipmentCid` since it needs to be reused
                user_e['data'] = id_to_data[user_e['equipmentCid']]
                res.append(user_e)
    return res

def get_ship_equips(cid):
    '''
    Given a ship's cid (integer), return all user owned equipment. 
    '''
    # 1. get corresponding equipmentType in shipCard by cid
    p = os.path.join(get_init_dir(), 'shipCard.json')
    with open(p, encoding='utf-8') as f:
        x = json.load(f)
    try:
        ship = next((i for i in x if i['cid'] == cid))
        # TOFIX
        types = ship['equipmentType']
    except StopIteration:
        return []

    return _type_to_equips(types)
"""

def get_ship_equips(cid):
    '''
    Given a ship's cid, find all user owned equipment.
    '''
    p = os.path.join(get_init_dir(), 'shipCard.json')
    with open(p, encoding='utf-8') as f:
        x = json.load(f)
    try:
        ship = next((i for i in x if i['cid']==cid))
    except StopIteration:
        return []

    target_type = ship['type']

    equip_path = os.path.join(get_init_dir(), 'shipEquipmnt.json')
    with open(equip_path, encoding='utf-8') as f1:
        all_equips = json.load(f1)

    equips = []
    id_to_data = {}
    for e in all_equips:
        if target_type in e['shipType']:
            equips.append(e['cid'])
            id_to_data[e['cid']] = process_one_equip(e)
        else:
            pass

    user_equip_path = os.path.join(get_user_dir(), 'equipmentVo.json')
    with open(user_equip_path, encoding='utf-8') as f2:
        user_equips = json.load(f2)

    res = []
    for e in equips:
        try:
            user_e = next((i for i in user_equips if i['equipmentCid'] == e))
            user_e.pop('uid')
        except StopIteration:
            continue

        if user_e['num'] > 0:
            user_e['data'] = id_to_data[user_e['equipmentCid']]
            res.append(user_e)
        else:
            continue
    return res

def update_equipment_amount(equipped, unequipped):
    # both input are cids (int)
    equipped = int(equipped)
    unequipped = int(unequipped)
    user_equip_path = os.path.join(get_user_dir(), 'equipmentVo.json')
    with open(user_equip_path, encoding='utf-8') as f:
        user_equips = json.load(f)
    if equipped == -1:      # unequip
        pass
    else:
        idx_1 = find_index(user_equips, 'equipmentCid', equipped)
        user_equips[idx_1]['num'] -= 1

    idx_2 = find_index(user_equips, 'equipmentCid', unequipped)
    user_equips[idx_2]['num'] += 1
    with open(user_equip_path, 'w', encoding='utf-8') as fout:
        json.dump(user_equips, fout, ensure_ascii=False, indent=4)


# ================================
# Tactics
# ================================


def get_tactics_json():
    path = os.path.join(get_init_dir(), 'ShipTactics.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_user_tactics():
    path = os.path.join(get_user_dir(), 'tactics.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t


# ================================
# Data processing
# ================================


def _process_shipItem():
    path = os.path.join(get_init_dir(), 'shipItem.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    
    res = {}
    for i in t:
        res[i['cid']] = i['title']
    return res

def init_ships_temp():
    data = {}
    path = os.path.join(get_temp_dir(), 'ship_id_to_info.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    else:
        card_path = os.path.join(get_init_dir(), 'shipCard.json')
        with open(card_path, encoding='utf-8') as f:
            cards = json.load(f)
        for c in cards:
            data[c['cid']] = {}
            data[c['cid']]['rarity'] = c['star']
            data[c['cid']]['country'] = c['country']
        with open(path, 'w', encoding='utf-8') as fout:
            json.dump(data, fout, ensure_ascii=False, indent=4)

    return data

def get_big_success_rate():
    path = os.path.join(get_user_dir(), 'userVo.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    res = int(t['detailInfo']['exploreBigSuccessNum']) / int(t['detailInfo']['exploreNum'])
    return round(res, 4)

# End of File