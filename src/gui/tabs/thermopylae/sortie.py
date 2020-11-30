import json

from time import sleep
from src.func.wgr_api import WGR_API
from logging import Logger


def save_json(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Sortie:
    def __init__(self, api: WGR_API, fleets: list, final_fleets: list, sortie_logger: Logger):
        super().__init__()
        self.api = api
        self.fleets = fleets # main fleets
        self.final_fleets = final_fleets # fill up required number of boats
        self.logger = sortie_logger

        self.pre_battle()
    '''
    Order:
    
    one time
        - six_getPveData
        - six_getFleetInfo
        - six_getuserdata
        - six_setChapterBoat
    on sub maps
        - six_readyFire
        - six_useAdjutant
        - six_withdraw
        - six_passLevel
    on each node
        - six_newNext
        - six_canSelectList
        - six_selectBoat
        - boat_supplyBoats
        - boat_instantRepairShips
        - six_spy
        - six_cha11enge
        - six_getWarResult
    others
        - six_adjutantExp
        - six_setWarFleet
    '''


    def pre_battle(self):
        self.logger.info('fuck pycharm')
        self.logger.info('get pve data')
        a = self.api.six_getPveData()
        save_json('a.json', a)
        sleep(2)
        self.logger.info('get fleet info')
        a = self.api.six_getFleetInfo()
        save_json('b.json', a)
        sleep(2)
        self.logger.info('get user data')
        a = self.api.six_getuserdata()
        save_json('c.json', a)
        sleep(2)

        print('fuck you pycharm')


# End of File