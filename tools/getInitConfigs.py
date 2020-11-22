#!/usr/bin/python
# -*- coding:utf-8 -*-
import pprint
import json
import tempfile


# url = 'http://login.jr.moefantasy.com/index/getInitConfigs'

tmp_path = tempfile.gettempdir()
import os
# print os.getenv('APPDATA')

def get_data():
    # TODO: following need to be executed once for new user.
    # Save chinese (instead of stupid unicode) into output file.
    with open('../getinitConfigs.json') as f:
        d = json.load(f)
        # Uncomment below to see output in terminal
        # pprint.pprint(d)

        # with open('full_getinitConfigs.txt', 'w', encoding='utf-8') as fout:
        #     json.dump(d, fout, ensure_ascii=False, indent=4)

        # with open('shipCard.json', 'w', encoding='utf-8') as fout:
            # json.dump(d['shipCard'], fout, ensure_ascii=False, indent=4)
        # print(d)
        f_ship = tempfile.TemporaryFile()
        # f_ship.write(d['shipCard'])
        f_ship.write(b'bitch')

        # with open('shipTactics.json', 'w', encoding='utf-8') as fout:
        #     json.dump(d['ShipTactics'], fout, ensure_ascii=False, indent=4)

        # with open('pveExplore.json', 'w', encoding='utf-8') as fout:
        #     json.dump(d['pveExplore'], fout, ensure_ascii=False, indent=4)

        # with open('shipEquipmnt.json', 'w', encoding='utf-8') as fout:
        #     json.dump(d['shipEquipmnt'], fout, ensure_ascii=False, indent=4)

        # with open('shipItem.json', 'w', encoding='utf-8') as fout:
        #     json.dump(d['shipItem'], fout, ensure_ascii=False, indent=4)

        # with open('shipCampaignLevel.json', 'w', encoding='utf-8') as fout:
        #     json.dump(d['shipCampaignLevel'], fout, ensure_ascii=False, indent=4)

        # with open('shipSkil1.json', 'w', encoding='utf-8') as fout:
        #     json.dump(d['shipSkil1'], fout, ensure_ascii=False, indent=4)

        # with open('errorCode.json', 'w', encoding='utf-8') as fout:
        #     json.dump(d['errorCode'], fout, ensure_ascii=False, indent=4)


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

# fff = type_equip_map(10000213)
# map_equip(fff)

get_data()