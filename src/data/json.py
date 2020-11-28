#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os

from .path import get_init_dir, get_user_dir, get_temp_dir

"""
Order functions alphabetically!
TODO: reduce code!
"""

def _load_json(folder, filename):
    path = os.path.join(folder, filename)
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_tactics_json():
    # return _load_json(get_init_dir(), 'ShipTactics.json')
    path = os.path.join(get_init_dir(), 'ShipTactics.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_user_fleets():
    path = os.path.join(get_user_dir(), 'fleetVo.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_user_tactics():
    path = os.path.join(get_user_dir(), 'tactics.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_processed_userShipVo():
    path = os.path.join(get_user_dir(), 'proc_userShipVo.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_shipItem():
    path = os.path.join(get_init_dir(), 'shipItem.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_userVo():
    path = os.path.join(get_user_dir(), 'userVo.json')
    with open(path, encoding='utf-8') as f:
        t = json.load(f)
    return t

def get_equipmentVo():
    # shipEquipmnt.json contains the equipment you own;
    # the `num` excludes those on ship
    user_equip_path = os.path.join(get_user_dir(), 'equipmentVo.json')
    with open(user_equip_path, encoding='utf-8') as f2:
        user_equips = json.load(f2)
    return user_equips

def save_equipmentVo(user_equips):
    user_equip_path = os.path.join(get_user_dir(), 'equipmentVo.json')
    with open(user_equip_path, 'w', encoding='utf-8') as fout:
        json.dump(user_equips, fout, ensure_ascii=False, indent=4)

def get_shipCard():
    p = os.path.join(get_init_dir(), 'shipCard.json')
    with open(p, encoding='utf-8') as f:
        x = json.load(f)
    return x

def get_shipEquipmnt(): # No typo
    equip_path = os.path.join(get_init_dir(), 'shipEquipmnt.json')
    with open(equip_path, encoding='utf-8') as f1:
        all_equips = json.load(f1)
    return all_equips

def save_processed_userShipVo(data):
    path = os.path.join(get_user_dir(), 'proc_userShipVo.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def init_ships_temp():
    data = {}
    path = os.path.join(get_temp_dir(), 'ship_cid_to_info.json')
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