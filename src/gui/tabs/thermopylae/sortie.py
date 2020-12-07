import json

from time import sleep
from src.wgr.api import WGR_API  # only for typehints
from src.exceptions.wgr_error import get_error
from src import data as wgr_data
from logging import Logger


def save_json(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Sortie:
    # This is only meant for who passed E6 with 6SS; will not considering doing E1-E5 in the near future
    # TODO long term
    # RIGHT NOW everything pre-battle is fixed
    def __init__(self, parent, api: WGR_API, fleets: list, final_fleets: list, sortie_logger: Logger, is_realrun: bool):
        super().__init__()
        self.parent = parent
        self.api = api
        self.fleets = fleets  # main fleets
        self.final_fleets = final_fleets  # fill up required number of boats
        self.logger = sortie_logger
        self.is_realrun = is_realrun
        self.sleep_time = 3

        self.fleet_info = None
        self.map_data = None
        self.user_data = None
        self.can_start = False
        self.boat_pool = []         # host existing boats
        self.escort_destroyers = []  # For 2DD to pass first few levels only, 萤火虫，布雷恩
        self.escort_carrier = -1  # For 1CV to pass first few levels only, 不挠
        self.points = -1
        self.init_map = "10006"
        self.init_sub_map = "9316"  # TODO
        self.user_ships = wgr_data.get_processed_userShipVo()

        self.logger.info("Init E6...")
        self.pre_battle()


    '''
    Order:
    
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
    levellist
    "levelId": "9314",
    "status": "3",  # sub map
    
    '''

    def pre_battle(self):
        self.logger.info("Start pre battle checking...")

        if self.is_realrun is True:
            # This is fast; no need for parallelism for now
            self.fleet_info = self.api.getFleetInfo()
            save_json('six_getFleetInfo.json', self.fleet_info)
            sleep(self.sleep_time)
            self.map_data = self.api.getPveData()
            save_json('six_getPveData.json', self.map_data)  # TODO only for testing
            sleep(self.sleep_time)
            self.user_data = self.api.getUserData()
            save_json('six_getUserData.json', self.user_data)  # TODO only for testing
            sleep(self.sleep_time)
        else:
            with open('six_getFleetInfo.json', 'r', encoding='utf-8') as f:
                self.fleet_info = json.load(f)
            with open('six_getPveData.json', 'r', encoding='utf-8') as f:
                self.map_data = json.load(f)
            with open('six_getUserData.json', 'r', encoding='utf-8') as f:
                self.user_data = json.load(f)

        self.can_start = self.set_info()
        if self.can_start is False:
            self.logger.warning("Failed to init pre-battle settings due to above reason.")
        else:
            self.logger.warning("Pre-battle settings is done.")

        self.logger.info("Setting final fleets:")
        for ship_id in self.final_fleets:
            ship = self.user_ships[str(ship_id)]
            output_str = f"{ship_id}, {ship['Name']}"
            if ship['Class'] == "SS":
                self.fleets.append(ship_id)
                output_str += ", MAIN FORCE"
            elif ship['cid'] in [11008211, 11009211]:  # TODO: fix this for now
                self.escort_destroyers.append(ship_id)
                output_str += ", ESCORT DD"
            elif ship['cid'] == 10031913:
                self.escort_carrier = ship_id
                output_str += ", ESCORT CV"
            # Lesson: do not output various stuff at once, concat them together; otherwise TypeError
            self.logger.info(output_str)

        self.get_curr_points()

        # TODO issue#82
        # data = self.api.setChapterBoat(self.init_map, self.final_fleets)
        # if 'eid' in data:
        #     get_error(data['eid'])
        # else:
        #     print(data)
        self.parent.sortie_button.setEnabled(True)

    def set_info(self) -> bool:

        # TODO free up dock space if needed
        user_e6 = next(i for i in self.user_data['chapterList'] if i['id'] == "10006")
        if self.user_data['levelId'] != "9316":
            self.logger.warning("You are in the middle of a battle. Exiting")
            return False
        elif self.user_data['npcId'] != "931821001":
            # Try to detect if user passed E6; TODO not sure if this is legit
            self.logger.warning("You have not passed E6 manually. Exiting")
            return False
        else:
            pass
        self.parent.update_ticket(self.user_data['ticket'])
        self.parent.update_purchasable(self.user_data['canChargeNum'])

        # check if the sortie "final fleet" is set or not
        b = self.fleet_info['chapterInfo']['boats']
        if len(b) == 0:
            self.logger.info('User has not entered E6. Select from old settings.')
            last_fleets = user_e6['boats']
        elif len(b) == 22 and self.fleet_info['chapterInfo']['level_id'] == "9316":
            # TODO long term; pick up where user left?
            self.logger.info('User has entered E6-1. Will retreat for a fresh start')
            last_fleets = b
        else:
            self.logger.info('Invalid settings for using this function.')
            self.logger.info('Ensure you have passed E6-3, AND you are not in a battle OR in E6-1.')
            return False

        self.points = self.user_data['strategic_point']
        if len(last_fleets) != 22:
            self.logger.warning("Invalid last boats settings.")
            res = False
        else:
            self.final_fleets = last_fleets
            res = True
        return res

    def start_sortie(self) -> None:
        self.logger.info('Retreating...')
        data = self.api.withdraw()
        if data is None:
            self.logger.info("Retreat success. Fresh start is ready.")
        else:
            pass

        data = self.api.readyFire(self.init_sub_map)
        if 'eid' in data:
            get_error(data['eid'])
            return
        else:
            next_node = self.get_next_node(data['$currentVo']['nodeId'])

        # get 11009211 and 11008211
        data = self.api.newNext(str(next_node))
        if 'eid' in data:
            get_error(data['eid'])
        else:
            pass

        self.get_ship_store()

        print(self.escort_destroyers)
        data = self.api.selectBoat(self.escort_destroyers)
        print(data)
        # print('buy one by one???')
        # data = self.api.selectBoat([self.escort_destroyers[0]])
        # print(data)
        # data = self.api.selectBoat([self.escort_destroyers[1]])
        # print(data)

    def get_ship_store(self, is_refresh: str = '0'):
        data = self.api.canSelectList(is_refresh)

        while '$ssss' not in data:
            self.logger.info('Getting ship store data again...')
            data = self.api.canSelectList(is_refresh)
            sleep(self.sleep_time)

        info = data['$ssss']
        for d in info:
            output_str = f'{self.user_ships[str(d[1])]} - LV {d[0]} - COST {d[2]}'
            self.logger.info(output_str)
        return data

    def get_next_node(self, node_id: str) -> int:
        node = next(i for i in self.map_data['combatLevelNode'] if i['id'] == node_id)
        # Always choose the upper path
        return node['next_node'][0]

    def get_curr_points(self):
        self.logger.info(f'Now have {self.points} strategic points left.')
        return self.points

# End of File
