from typing import Tuple, Any
from time import time

from src.data.wgv_json import (
    get_user_fleets, get_shipItem, get_userVo,
    get_shipCard, get_shipEquipmnt, get_equipmentVo,
    save_equipmentVo, get_pveExploreVo
)


# ================================
# Not Exports
# ================================


def _process_one_equip(equip: dict) -> dict:
    res = {'title': equip['title'], 'desc': equip['desc']}
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


def _process_shipItem() -> dict:
    t = get_shipItem()
    res = {}
    for i in t:
        res[i['cid']] = i['title']
    return res


# ================================
# Exports
# ================================


def get_big_success_rate() -> Tuple[float, int, int]:
    t = get_userVo()
    n = int(t['detailInfo']['exploreBigSuccessNum'])
    d = int(t['detailInfo']['exploreNum'])
    res = round(n / d, 4)
    return res, n, d


def get_exp_fleets() -> dict:
    # return a list of int
    fleets = get_user_fleets()
    exp_ids = ["5", "6", "7", "8"]
    res = {}
    for fleet in fleets:
        if fleet['id'] in exp_ids:
            res[fleet['id']] = fleet['ships']
        else:
            continue
    return res


def get_ship_equips(cid: int) -> list:
    """
    Given a ship's cid, find all user owned equipment.
    """
    x = get_shipCard()
    try:
        ship = next((i for i in x if i['cid'] == cid))
    except StopIteration:
        return []

    target_type = ship['type']

    all_equips = get_shipEquipmnt()
    equips = []
    id_to_data = {}
    for e in all_equips:
        if target_type in e['shipType']:
            equips.append(e['cid'])
            id_to_data[e['cid']] = _process_one_equip(e)
        else:
            pass

    user_equips = get_equipmentVo()
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


def get_exp_map(fleet_id: str) -> str:
    """
    Given a fleet id, return expedition-able maps.
        If none, return '1-1'.
    @param fleet_id: fleet id, str form of int, ranging from 4 to 8
    @type fleet_id: str
    @return: Normally accepted representation of str
    @rtype: str
    """
    _json = get_pveExploreVo()['levels']
    try:
        fleet = next(i for i in _json if i['fleetId'] == fleet_id)
        map_name = fleet['exploreId'].replace('000', '-')
    except StopIteration:
        map_name = '1-1'
    return map_name


def get_exp_list() -> list:
    exp_list = get_pveExploreVo()['chapters']
    res = []
    for i in exp_list:
        end_idx = 5 if i != 8 else 3
        _list = [str(i) + '-' + str(j) for j in range(1, end_idx)]
        res += _list
    return res


def is_exp_done(fleet_id: str) -> bool:
    """
    Given a fleet id, return the status of current fleet
    @param fleet_id: fleet id, str form of int, ranging from 4 to 8
    @type fleet_id: str
    @return: return True if the expedition is done; otherwise False
    @rtype: bool
    """
    _json = get_pveExploreVo()['levels']
    try:
        fleet = next(i for i in _json if i['fleetId'] == fleet_id)
        res = fleet['endTime'] > int(time())
    except StopIteration:
        res = False
    return res


def get_love_list():
    # url = self.server + 'api/getShipList' + hlp.get_url_end()
    # raw_data = self.decompress_data(url)
    # data = json.loads(raw_data)
    # x = data["userShipVO"]
    # x.sort(key=lambda y:y["level"], reverse=True)
    # counter = 0
    # for s in x:
    #     if (int(s["love"]) > 60) and (s["love"] != s["loveMax"]) and (s["loveMax"] == 100):
    #         print("{}. {}\t{}\t{}\t{}/{}".format(counter, s["id"], s["title"], s["level"], s["love"], s["loveMax"]))
    #         time.sleep(3)
    #         url = self.server + 'friend/kiss/' + str(s["id"]) + hlp.get_url_end()
    #         raw_data = self.decompress_data(url)
    #         data = json.loads(raw_data)
    #         print(data)
    #         try:
    #             if "love" in data["shipVO"]:
    #                 counter += 1
    #                 print("kiss success")
    #         except KeyError:
    #             pass
    #     if counter >= 5:
    #         break
    raise NotImplementedError


def update_equipment_amount(equipped: int, unequipped: int) -> None:
    equipped = int(equipped)
    unequipped = int(unequipped)
    user_equips = get_equipmentVo()
    if equipped == -1:  # unequip
        pass
    else:
        idx_1 = find_index(user_equips, 'equipmentCid', equipped)
        user_equips[idx_1]['num'] -= 1

    idx_2 = find_index(user_equips, 'equipmentCid', unequipped)
    user_equips[idx_2]['num'] += 1
    save_equipmentVo(user_equips)


def find_index(_list: list, key: Any, value: Any) -> int:
    """
    Given a list of dict, find index by key-value pair.
    """
    for i, _dict in enumerate(_list):
        if _dict[key] == value:
            return i
    return -1


def find_all_indices(_list, key: Any, value: Any) -> list:
    res = []
    for i, _dict in enumerate(_list):
        if _dict[key] == value:
            res.append(i)
    return res


""" Following implementation is not used because Moefantasy bug
def _type_to_equips(equipment_types):
    '''
    Based on a ship equipment types, return all user owned equipment. 
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
        id_to_data[e['cid']] = _process_one_equip(e)

    print(type_to_id)

    user_equip_path = os.path.join(get_user_dir(), 'equipmentVo.json')
    with open(user_equip_path, encoding='utf-8') as f2:
        user_equips = json.load(f2)

    # 3. get all user-owned equipment by equipment id
    res = []
    for t in equipment_types:
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
        types = ship['equipmentType']
    except StopIteration:
        return []

    return _type_to_equips(types)
"""

# End of File
