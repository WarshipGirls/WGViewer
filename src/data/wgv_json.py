#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os

from .wgv_path import get_init_dir, get_user_dir, get_temp_dir

"""
Order functions alphabetically!
"""


# ================================
# Not Exports
# ================================

def _load_json(folder, filename):
    path = os.path.join(folder, filename)
    with open(path, encoding='utf-8') as fin:
        t = json.load(fin)
    return t


def _save_json(folder, filename, data):
    path = os.path.join(folder, filename)
    with open(path, 'w', encoding='utf-8') as fout:
        json.dump(data, fout, ensure_ascii=False, indent=4)


# ================================
# Exports
# ================================

def get_api_initGame():
    return _load_json(get_temp_dir(), 'api_initGame.json')


def save_api_initGame(data):
    _save_json(get_temp_dir(), 'api_initGame.json', data)


def get_api_getShipList():
    return _load_json(get_temp_dir(), 'api_getShipList.json')


def save_api_getShipList(data):
    _save_json(get_temp_dir(), 'api_getShipList.json', data)


def get_equipmentVo():
    # shipEquipmnt.json contains the equipment you own;
    # the `num` excludes those on ship
    return _load_json(get_user_dir(), 'equipmentVo.json')


def save_equipmentVo(data):
    _save_json(get_user_dir(), 'equipmentVo.json', data)


def get_processed_userShipVo():
    return _load_json(get_user_dir(), 'proc_userShipVo.json')


def save_processed_userShipVo(data):
    _save_json(get_user_dir(), 'proc_userShipVo.json', data)


def get_pveExploreVo():
    return _load_json(get_user_dir(), 'get_pveExploreVo.json')


def save_pveExploreVo(data):
    _save_json(get_user_dir(), 'get_pveExploreVo.json', data)


def get_shipCard():
    return _load_json(get_init_dir(), 'shipCard.json')


def get_shipEquipmnt():  # No typo
    return _load_json(get_init_dir(), 'shipEquipmnt.json')


def get_shipItem():
    return _load_json(get_init_dir(), 'shipItem.json')


def get_tactics_json():
    return _load_json(get_init_dir(), 'ShipTactics.json')


def get_taskVo():
    return _load_json(get_init_dir(), 'taskVo.json')


def save_taskVo(data):
    _save_json(get_user_dir(), 'taskVo.json', data)


def get_user_fleets():
    return _load_json(get_user_dir(), 'fleetVo.json')


def save_user_fleets(data):
    _save_json(get_user_dir(), 'fleetVo.json', data)


def get_user_tactics():
    return _load_json(get_user_dir(), 'tactics.json')


def save_user_tactics(data):
    _save_json(get_user_dir(), 'tactics.json', data)


def get_userVo():
    return _load_json(get_user_dir(), 'userVo.json')


def save_userVo(data):
    _save_json(get_user_dir(), 'userVo.json', data)


def init_ships_temp():
    data = {}
    path = os.path.join(get_temp_dir(), 'ship_cid_to_info.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    else:
        cards = get_shipCard()
        for c in cards:
            # Due to json.dump, key will be convert to str type anyway
            data[str(c['cid'])] = {}
            data[str(c['cid'])]['rarity'] = c['star']
            data[str(c['cid'])]['country'] = c['country']
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    return data

# End of File
