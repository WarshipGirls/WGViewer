#!/usr/bin/python
# -*- coding:utf-8 -*-
import pprint
import json

# url = 'http://login.jr.moefantasy.com/index/getInitConfigs'

# Save chinese (instead of stupid unicode) into output file.
with open('../getinitConfigs.json') as f:
    d = json.load(f)
    # Uncomment below to see output in terminal
    # pprint.pprint(d)

    # with open('full_getinitConfigs.txt', 'w', encoding='utf-8') as fout:
    #     json.dump(d, fout, ensure_ascii=False, indent=4)

    with open('shipCard.json', 'w', encoding='utf-8') as fout:
        json.dump(d['shipCard'], fout, ensure_ascii=False, indent=4)

    with open('shipTactics.json', 'w', encoding='utf-8') as fout:
        json.dump(d['ShipTactics'], fout, ensure_ascii=False, indent=4)

    with open('pveExplore.json', 'w', encoding='utf-8') as fout:
        json.dump(d['pveExplore'], fout, ensure_ascii=False, indent=4)

    with open('shipEquipmnt.json', 'w', encoding='utf-8') as fout:
        json.dump(d['shipEquipmnt'], fout, ensure_ascii=False, indent=4)

    with open('shipItem.json', 'w', encoding='utf-8') as fout:
        json.dump(d['shipItem'], fout, ensure_ascii=False, indent=4)

    with open('shipCampaignLevel.json', 'w', encoding='utf-8') as fout:
        json.dump(d['shipCampaignLevel'], fout, ensure_ascii=False, indent=4)

    with open('shipSkil1.json', 'w', encoding='utf-8') as fout:
        json.dump(d['shipSkil1'], fout, ensure_ascii=False, indent=4)

    with open('errorCode.json', 'w', encoding='utf-8') as fout:
        json.dump(d['errorCode'], fout, ensure_ascii=False, indent=4)