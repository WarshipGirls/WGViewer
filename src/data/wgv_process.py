from .wgv_json import (
    get_user_fleets, get_shipItem, get_userVo,
    get_shipCard, get_shipEquipmnt, get_equipmentVo,
    save_equipmentVo, get_pveExploreVo
)


# ================================
# Not Exports
# ================================

def _process_one_equip(equip):
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


def _process_shipItem():
    t = get_shipItem()
    res = {}
    for i in t:
        res[i['cid']] = i['title']
    return res


# ================================
# Exports
# ================================

def get_big_success_rate():
    t = get_userVo()
    n = t['detailInfo']['exploreBigSuccessNum']
    d = t['detailInfo']['exploreNum']
    res = round(int(n) / int(d), 4)
    return [res, n, d]


def get_exp_fleets():
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


def get_ship_equips(cid):
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


def get_exp_map(fleet_id):
    _json = get_pveExploreVo()['levels']
    try:
        fleet = next(i for i in _json if i['fleetId'] == str(fleet_id))
        map_name = fleet['exploreId'].replace('000', '-')
    except StopIteration:
        map_name = ""
    return map_name


def get_exp_list():
    exp_list = get_pveExploreVo()['chapters']
    res = []
    for i in exp_list:
        end_idx = 5 if i is not 8 else 3
        _list = [str(i) + "000" + str(j) for j in range(1, end_idx)]
        res += _list
    return res


def update_equipment_amount(equipped, unequipped):
    # both input are cid (int)
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


def find_index(lst, key, value):
    """
    Given a list of dict, find index by key-value pair.
    """
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
