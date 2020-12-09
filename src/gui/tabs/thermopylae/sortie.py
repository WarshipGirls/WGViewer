import json

from time import sleep
from logging import getLogger
from typing import Tuple

from src import data as wgv_data
from src.exceptions.custom import ThermopylaeSoriteExit
from .helper import SortieHelper

# Following are only for typehints
from src.wgr.six import API_SIX


def save_json(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Sortie:
    # This is only meant for who passed E6 with 6SS; will not considering doing E1-E5 in the near future
    # TODO long term
    # RIGHT NOW everything pre-battle is fixed

    def __init__(self, parent, api: API_SIX, fleets: list, final_fleets: list, is_realrun: bool):
        super().__init__()
        self.parent = parent
        self.api: API_SIX = api
        self.fleets = fleets  # main fleets
        self.final_fleets = final_fleets  # fill up required number of boats
        self.logger = getLogger('TabThermopylae')
        self.is_realrun = is_realrun

        self.sleep_time = 3  # TODO random this every time
        self.max_retry = 5

        self.fleet_info = None
        self.map_data = None
        self.user_data = None
        self.can_start = False
        self.helper = None
        self.repair_level = 1
        self.boat_pool = []  # host existing boats
        self.escort_DD = []  # For 2DD to pass first few levels only, 萤火虫，布雷恩
        self.escort_CV = []  # For 1CV to pass first few levels only, 不挠
        self.user_ships = wgv_data.get_processed_userShipVo()

        self.logger.info("Init E6...")

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

    def _get_fleet_info(self) -> None:
        if self.is_realrun is True:
            self.fleet_info = self.api.getFleetInfo()
            # save_json('six_getFleetInfo.json', self.fleet_info)  # TODO only for testing; delete later
            sleep(self.sleep_time)
        else:
            with open('six_getFleetInfo.json', 'r', encoding='utf-8') as f:
                self.fleet_info = json.load(f)

    def _get_pve_data(self) -> None:
        if self.is_realrun is True:
            self.map_data = self.api.getPveData()
            # save_json('six_getPveData.json', self.map_data)  # TODO only for testing
            sleep(self.sleep_time)
        else:
            with open('six_getPveData.json', 'r', encoding='utf-8') as f:
                self.map_data = json.load(f)

    def _get_user_data(self) -> None:
        if self.is_realrun is True:
            self.user_data = self.api.getUserData()
            # save_json('six_getUserData.json', self.user_data)  # TODO only for testing
            sleep(self.sleep_time)
        else:
            with open('six_getUserData.json', 'r', encoding='utf-8') as f:
                self.user_data = json.load(f)

    def pre_battle_calls(self) -> bool:
        self._get_fleet_info()
        self._get_pve_data()
        self._get_user_data()

        self.can_start = self.pre_battle_set_info()
        if self.can_start is False:
            self.logger.warning("Failed to pre-battle checking due to above reason.")
        else:
            self.logger.warning("Pre-battle checking is done.")
        return self.can_start

    def pre_battle(self) -> None:
        self.logger.info("Start pre battle checking...")

        if self.pre_battle_calls() is False:
            return

        self.helper = SortieHelper(self.api, self.user_ships, self.map_data)

        self.logger.info("Setting final fleets:")
        for ship_id in self.final_fleets:
            ship = self.user_ships[str(ship_id)]
            output_str = "{:8s}{:17s}".format(str(ship_id), ship['Name'])
            if ship['Class'] == "SS":
                self.fleets.append(ship_id)
                output_str += "\tMAIN FORCE"
            elif ship['cid'] in [11008211, 11009211]:  # TODO: fix this for now
                self.escort_DD.append(ship_id)
                output_str += "\tESCORT DD"
            elif ship['cid'] in [10031913]:
                self.escort_CV.append(ship_id)
                output_str += "\tESCORT CV"
            # Lesson: do not output various stuff at once, concat them together; otherwise TypeError
            self.logger.info(output_str)

        self.parent.button_sortie.setEnabled(True)

    def pre_battle_set_info(self) -> bool:
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
            self.logger.info('User has not entered E6. Select from old settings')
            last_fleets = user_e6['boats']
        elif len(b) == 22 and self.fleet_info['chapterInfo']['level_id'] == "9316":
            # TODO long term; pick up where user left?
            self.logger.info('User has entered E6-1. Will retreat for a fresh start')
            last_fleets = b
        else:
            self.logger.info('Invalid settings for using this function')
            self.logger.info('Ensure you have passed E6-3, AND you are not in a battle OR in E6-1')
            return False

        if len(last_fleets) != 22:
            self.logger.warning("Invalid last boats settings.")
            res = False
        else:
            self.final_fleets = last_fleets
            res = True
        return res

    def start_sortie(self) -> None:
        self.logger.info('Retreating...')
        try:
            next_id, next_name = self.E6_1_A1_sortie()
            print(next_id, next_name)
        except ThermopylaeSoriteExit:
            self.parent.button_sortie.setEnabled(True)
            return

    def E6_1_A1_sortie(self) -> Tuple[str, str]:
        self.helper.api_withdraw()
        next_node_id = self.helper.api_readyFire()
        self.helper.api_newNext(str(next_node_id))

        shop_data = self.helper.get_ship_store()
        buy_data = self.helper.buy_ships(self.escort_DD, shop_data)
        # TODO dynamically update boat pool info on left panel
        self.boat_pool = buy_data['boatPool']
        self.helper.set_war_fleets(self.escort_DD)

        # Node E6-1 A1, lv.1 -> lv.2
        adj_data = self.helper.cast_skill()
        if self.helper.bump_level(adj_data) is False:
            self.logger.info('Bumping failed. Should restart current sub-map.')
        else:
            pass

        sp_res = self.helper.supply_boats(self.escort_DD)
        self.parent.update_resources(sp_res['userVo']['oil'], sp_res['userVo']['ammo'], sp_res['userVo']['steel'], sp_res['userVo']['aluminium'])

        self.helper.process_repair(sp_res['shipVO'], [1])   # pre-battle repair
        sleep(2)
        self.helper.spy()
        sleep(2)
        challenge_res = self.helper.challenge('1')
        do_night_battle = self.helper.is_night_battle(challenge_res)
        sleep(10)
        if do_night_battle is True:
            battle_res = self.helper.get_war_result('1')
        else:
            battle_res = self.helper.get_war_result('0')
        self.helper.process_battle_result(battle_res)
        sleep(3)
        self.helper.process_repair(battle_res['shipVO'], [1])   # post-battle repair
        if int(battle_res['getScore$return']['flagKill']) == 1 or battle_res['resultLevel'] in [1, 2]:
            next_id, next_name = self.helper.get_next_node_by_id(battle_res['nodeInfo']['node_id'])
        else:
            self.logger.info('Failed to clean E6-1 A1. Should restart. Exiting.')
            next_id = -1
            next_name = "??"
        return next_id, next_name


# End of File
