#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os


# ================================
# Not Exports
# ================================

def _load_json(folder: str, filename: str) -> [list, dict]:
    path = os.path.join(folder, filename)
    with open(path, 'r', encoding='utf-8') as fin:
        t = json.load(fin)
    return t


def _save_json(folder: str, filename: str, data: [list, dict]) -> None:
    path = os.path.join(folder, filename)
    with open(path, 'w', encoding='utf-8') as fout:
        json.dump(data, fout, ensure_ascii=False, indent=4)


# ================================
# Exports
# ================================


def get_api_initGame() -> dict:
    return _load_json(get_temp_dir(), 'api_initGame.json')


def save_api_initGame(data: dict) -> None:
    _save_json(get_temp_dir(), 'api_initGame.json', data)


def get_api_getShipList() -> dict:
    return _load_json(get_temp_dir(), 'api_getShipList.json')


def save_api_getShipList(data: dict) -> None:
    _save_json(get_temp_dir(), 'api_getShipList.json', data)


def get_equipmentVo() -> list:
    # shipEquipmnt.json contains the equipment you own;
    # the `num` excludes those on ship
    return _load_json(get_user_dir(), 'equipmentVo.json')


def save_equipmentVo(data: list) -> None:
    _save_json(get_user_dir(), 'equipmentVo.json', data)


def get_processed_userShipVo() -> dict:
    return _load_json(get_user_dir(), 'proc_userShipVo.json')


def save_processed_userShipVo(data: dict) -> None:
    _save_json(get_user_dir(), 'proc_userShipVo.json', data)


def get_pveExploreVo() -> dict:
    return _load_json(get_user_dir(), 'get_pveExploreVo.json')


def save_pveExploreVo(data: dict) -> None:
    _save_json(get_user_dir(), 'get_pveExploreVo.json', data)


def get_shipCard() -> dict:
    return _load_json(get_init_dir(), 'shipCard.json')


def get_shipEquipmnt() -> dict:  # No typo
    return _load_json(get_init_dir(), 'shipEquipmnt.json')


def get_shipItem() -> dict:
    return _load_json(get_init_dir(), 'shipItem.json')


def get_tactics_json() -> dict:
    return _load_json(get_init_dir(), 'ShipTactics.json')


def get_taskVo() -> dict:
    return _load_json(get_init_dir(), 'taskVo.json')


def save_taskVo(data: dict) -> None:
    _save_json(get_user_dir(), 'taskVo.json', data)


def get_user_fleets() -> dict:
    return _load_json(get_user_dir(), 'fleetVo.json')


def save_user_fleets(data: dict) -> None:
    _save_json(get_user_dir(), 'fleetVo.json', data)


def get_user_tactics() -> dict:
    return _load_json(get_user_dir(), 'tactics.json')


def save_user_tactics(data: dict) -> None:
    _save_json(get_user_dir(), 'tactics.json', data)


def get_userVo() -> dict:
    return _load_json(get_user_dir(), 'userVo.json')


def save_userVo(data: dict) -> None:
    _save_json(get_user_dir(), 'userVo.json', data)


def init_ships_temp() -> dict:
    data = {}
    path = os.path.join(get_temp_dir(), 'ship_cid_to_info.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    else:
        cards = get_shipCard()
        for c in cards:
            if 'cost' in c:
                # card without 'cost' is enemy cards
                # Due to json.dump, key will be convert to str type anyway
                data[str(c['cid'])] = {}
                data[str(c['cid'])]['rarity'] = c['star']
                data[str(c['cid'])]['country'] = c['country']
                data[str(c['cid'])]['cost'] = c['cost']
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    return data


if __name__ == "__main__":
    from src.data.wgv_path import get_init_dir, get_user_dir, get_temp_dir, get_data_dir
else:
    from .wgv_path import get_init_dir, get_user_dir, get_temp_dir, get_data_dir

# End of File
