import json

from time import sleep
from src.wgr.api import WGR_API  # only for typehints
from src.utils import popup_msg
from logging import Logger


def save_json(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Sortie:
    # This is only meant for who passed E6 with 6SS; will not considering doing E1-E5 in the near future
    # TODO long term
    def __init__(self, parent, api: WGR_API, fleets: list, final_fleets: list, sortie_logger: Logger):
        super().__init__()
        self.parent = parent
        self.api = api
        self.fleets = fleets  # main fleets
        self.final_fleets = final_fleets  # fill up required number of boats
        self.logger = sortie_logger

        self.user_data = None
        self.fleets = None
        self.can_start = False
        self.logger.info("Start E6 sortieing...")
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
    
    > self.user_data
    nodeId: highest reached node: 913821 E6-boss
    levelId: highest reached map: 9318 (E6 map3)
    adjutantList: 10082, 10182, 10282
    chapterList
        -> id : 10001 (E1) ... 10006 (E6)
        -> status: ( I believe this is the user current map )
            1 (sub map 1), ..., 3 (sub map 3)
        -> boats:
            last set boat
            len E1/2 = 14, E3/4 = 18, E5/6 = 22
        -> level_id  ( I believe this is the user reached level)
            9301 (E1 map1) 9303 (E1 map3) 9304 (E2 map1) 9316 (E6 map 1)
    
    '''

    def pre_battle(self):
        # TODO under dev
        self.logger.info("Start pre battle checking...")
        # a = self.api.getPveData()
        # save_json('a.json', a)
        # sleep(2)
        # self.logger.info('get fleet info')
        # a = self.api.getFleetInfo()
        # save_json('b.json', a)
        # sleep(2)

        # self.logger.info('get user data')
        # self.user_data = self.api.getUserdata()
        # with open('c.json', 'r', encoding='utf-8') as f:
        with open('c.json', 'r') as f:
            self.user_data = json.load(f)
        # save_json('c.json', a)
        # sleep(2)

        self.can_start = self.set_info()
        if self.can_start is False:
            self.logger.warning("You have not passed E6, which disqualified you for using this function. Exiting")
        else:
            self.logger.warning("Pre-battle settings is done.")

    def set_info(self) -> bool:
        res = False
        if self.user_data['levelId'] != "9318":
            self.logger.warning("You have not passed E6 manually.")
            res = False
        else:
            res = True
        self.parent.update_ticket(self.user_data['ticket'])
        self.parent.update_purchasable(self.user_data['canChargeNum'])
        last_fleets = next(i for i in self.user_data['chapterList'] if i['id'] == "10006")['boats']
        if len(last_fleets) != 22:
            self.logger.warning("Invalid last boats settings.")
            res = False
        else:
            res = True
        return res

# End of File
