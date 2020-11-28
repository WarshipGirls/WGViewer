#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os

from .path import get_init_dir, get_user_dir, get_temp_dir

"""
Order functions alphabetically!
"""

def _load_json(folder, filename):
    path = os.path.join(folder, filename)
    with open(path, encoding='utf-8') as fin:
        t = json.load(fin)
    return t

def _save_json(folder, filename, data):
    path = os.path.join(folder, filename)
    with open(path, 'w', encoding='utf-8') as fout:
        json.dump(data, fout, ensure_ascii=False, indent=4)

def get_tactics_json():
    return _load_json(get_init_dir(), 'ShipTactics.json')

def get_user_fleets():
    return _load_json(get_user_dir(), 'fleetVo.json')

def get_user_tactics():
    return _load_json(get_user_dir(), 'tactics.json')

def get_processed_userShipVo():
    return _load_json(get_user_dir(), 'proc_userShipVo.json')

def get_shipItem():
    return _load_json(get_init_dir(), 'shipItem.json')

def get_userVo():
    return _load_json(get_user_dir(), 'userVo.json')

def get_equipmentVo():
    # shipEquipmnt.json contains the equipment you own;
    # the `num` excludes those on ship
    return _load_json(get_user_dir(), 'equipmentVo.json')

def save_equipmentVo(user_equips):
    _save_json(get_user_dir(), 'equipmentVo.json', user_equips)

def get_shipCard():
    return _load_json(get_init_dir(), 'shipCard.json')

def get_shipEquipmnt(): # No typo
    return _load_json(get_init_dir(), 'shipEquipmnt.json')

def save_processed_userShipVo(data):
    _save_json(get_user_dir(), 'proc_userShipVo.json', data)

def init_ships_temp():
    data = {}
    path = os.path.join(get_temp_dir(), 'ship_cid_to_info.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    else:
        cards = get_shipCard()
        for c in cards:
            data[c['cid']] = {}
            data[c['cid']]['rarity'] = c['star']
            data[c['cid']]['country'] = c['country']
        with open(path, 'w', encoding='utf-8') as fout:
            json.dump(data, fout, ensure_ascii=False, indent=4)

    return data


# End of File