import json

from logging import getLogger
from typing import Tuple

from src import data as wgv_data
from src.utils.general import set_sleep
from src.exceptions.custom import ThermopylaeSoriteExit
from .helper import SortieHelper

# Following are only for typehints
from src.wgr.six import API_SIX

ADJUTANT_ID_TO_NAME = {
    '10082': "紫貂",
    '10182': "Kearsarge",
    '10282': "Habakkuk"
}


def save_json(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Sortie:
    # This is only meant for who passed E6 with 6SS; will not considering doing E1-E5 in the near future
    # TODO long term
    # RIGHT NOW everything pre-battle is fixed

    # SINCE game version 5.1.0, only 5 slots is shown; E6-1 A1 can choose 5 ships; after that, it's 4 ships + buff card

    def __init__(self, parent, api: API_SIX, fleet: list, final_fleet: list, is_realrun: bool):
        super().__init__()
        self.parent = parent
        self.api: API_SIX = api
        self.main_fleet = fleet  # main fleets (6SS)
        self.battle_fleet = []  # ships that on battle
        self.final_fleet = final_fleet  # fill up required number of boats
        self.logger = getLogger('TabThermopylae')
        self.is_realrun = is_realrun

        self.max_retry = 5

        self.fleet_info = None
        self.map_data = None
        self.user_data = None
        self.can_start = False
        self.helper = None
        self.repair_level = 1
        self.curr_node = "0"
        self.boat_pool = []  # host existing boats
        self.escort_DD = []  # For 2DD to pass first few levels only, 萤火虫，布雷恩
        self.escort_CV = []  # For 1CV to pass first few levels only, 不挠
        self.user_ships = wgv_data.get_processed_userShipVo()

        self.logger.info("Init E6...")

    '''
    > self.user_data
        -> nodeId: current node
        -> levelId: current level
        -> chapterId: current chapter
        -> npcId: current enemy
        -> boats:
            last set boat
            len E1/2 = 14, E3/4 = 18, E5/6 = 22
        -> level_id  ( I believe this is the user reached level)
            9301 (E1 map1) 9303 (E1 map3) 9304 (E2 map1) 9316 (E6 map 1)
    levellist
    "levelId": "9314",
    "status": "3",  # sub map
    
    '''

    # ================================
    # Pre battle checke
    # ================================

    def _get_fleet_info(self) -> None:
        if self.is_realrun is True:
            self.fleet_info = self.api.getFleetInfo()
            save_json('six_getFleetInfo.json', self.fleet_info)  # TODO only for testing; delete later
            set_sleep()
        else:
            with open('six_getFleetInfo.json', 'r', encoding='utf-8') as f:
                self.fleet_info = json.load(f)

    def _get_pve_data(self) -> None:
        if self.is_realrun is True:
            self.map_data = self.api.getPveData()
            save_json('six_getPveData.json', self.map_data)  # TODO only for testing
            set_sleep()
        else:
            with open('six_getPveData.json', 'r', encoding='utf-8') as f:
                self.map_data = json.load(f)

    def _get_user_data(self) -> None:
        if self.is_realrun is True:
            self.user_data = self.api.getUserData()
            save_json('six_getUserData.json', self.user_data)  # TODO only for testing
            set_sleep()
        else:
            with open('six_getUserData.json', 'r', encoding='utf-8') as f:
                self.user_data = json.load(f)

    def pre_battle_set_info(self) -> bool:
        # TODO free up dock space if needed
        user_e6 = next(i for i in self.user_data['chapterList'] if i['id'] == "10006")
        if self.user_data['chapterId'] != '10006':
            self.logger.warning("You are in the middle of a battle other than E6. Exiting")
            return False
        elif len(user_e6['boats']) != 22:
            # Try to detect if user passed E6;
            self.logger.warning("You have not passed E6 manually. Exiting")
            return False
        else:
            pass
        self.set_sortie_tickets()
        self.set_adjutant_info()

        # check if the sortie "final fleet" is set or not
        b = self.fleet_info['chapterInfo']['boats']
        if len(b) == 0:
            self.logger.info('User has not entered E6. Select from old settings')
            last_fleets = user_e6['boats']
        elif len(b) == 22 and self.fleet_info['chapterInfo']['level_id'] == "9316":
            self.logger.info('User has entered E6-1.')
            last_fleets = b
        else:
            self.logger.info('Invalid settings for using this function')
            self.logger.info('1. Ensure you have cleared E6-3; 2. You are not in a battle OR in E6')
            return False

        self.set_boat_pool(self.fleet_info['fleet'])
        self.curr_node = str(self.user_data['nodeId'])

        if len(last_fleets) != 22:
            self.logger.warning("Invalid last boats settings.")
            res = False
        else:
            self.final_fleet = last_fleets
            res = True
        return res

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

        self.helper = SortieHelper(self.parent, self.api, self.user_ships, self.map_data)
        self.helper.set_adjutant_info(self.user_data['adjutantData'])
        self.helper.set_curr_points(self.user_data['strategic_point'])

        self.logger.info("Setting final fleets:")
        for ship_id in self.final_fleet:
            ship = self.user_ships[str(ship_id)]
            output_str = "{:8s}{:17s}".format(str(ship_id), ship['Name'])
            if ship['Class'] == "SS":
                self.main_fleet.append(ship_id)
                output_str += "\tMAIN FORCE"
            elif ship['cid'] in [11008211, 11009211]:  # TODO: fix this for now
                self.escort_DD.append(ship_id)
                output_str += "\tESCORT DD"
            elif ship['cid'] in [10031913]:
                self.escort_CV.append(ship_id)
                output_str += "\tESCORT CV"
            # Lesson: do not output various stuff at once, concat them together; otherwise TypeError
            self.logger.info(output_str)

        self.parent.button_fresh_sortie.setEnabled(True)
        if len(self.boat_pool) > 0:
            self.parent.button_resume_sortie.setEnabled(True)
            self.logger.info('Can choose a fresh start or resume existing battle')
        else:
            self.logger.info('Can choose a fresh start')

    # ================================
    # Entry points
    # ================================

    def resume_sortie(self) -> None:
        self.logger.info(f"Resume sortie from node {self.curr_node}")
        try:
            if self.curr_node == '931602':
                next_id = self.E6_1_B1_sortie(self.curr_node)
        except ThermopylaeSoriteExit:
            self.parent.button_fresh_sortie.setEnabled(True)
            return

    def start_fresh_sortie(self) -> None:
        self.logger.info('Retreating...')
        try:
            next_id = self.E6A1()
            # next_id = self.E6_1_A1_sortie()
            # self.curr_node = next_id
            # self.E6_1_B1_sortie(self.curr_node)
            while next_id != "931617":
                next_id = self.single_node_sortie(next_id)
        except ThermopylaeSoriteExit:
            self.parent.button_fresh_sortie.setEnabled(True)
            return

    # ================================
    # Setter / Getter
    # ================================

    def set_sortie_tickets(self) -> None:
        self.parent.update_ticket(self.user_data['ticket'])
        self.parent.update_purchasable(self.user_data['canChargeNum'])

    def set_adjutant_info(self) -> None:
        # TODO: very similar functions in helper.py; may remove one of them
        adj = self.user_data['adjutantData']
        self.parent.update_adjutant_name(ADJUTANT_ID_TO_NAME[adj['id']])
        self.parent.update_adjutant_exp(f"Lv. {adj['level']} {adj['exp']}/{adj['exp_top']}")
        self.parent.update_points(str(self.user_data['strategic_point']))

    def set_boat_pool(self, boat_pool: list) -> None:
        self.boat_pool = boat_pool
        label_text = "Selected ships: "
        for s in self.boat_pool:
            label_text += f"{self.user_ships[s]['Name']} "
        self.parent.update_boat_pool_label(label_text)

    def set_fleets(self, fleet: list) -> None:
        # The list may contain string or integer elements
        try:
            assert (len(fleet) <= 6)
            label_text = "On battle: "
            i = 1
            ss_count = 0
            ss = []
            for s in fleet:
                label_text += f"{i} {self.user_ships[s]['Name']} "
                if self.user_ships[s]['Class'] == "SS":
                    ss_count += 1
                    ss.append(s)
                i += 1
            self.parent.update_fleet_label(label_text)
            if ss_count >= 4:
                self.battle_fleet = [int(j) for j in ss]
            else:
                self.battle_fleet = [int(j) for j in fleet]
        except AssertionError:
            raise ThermopylaeSoriteExit

    def set_side_dock_resources(self, x):
        self.parent.update_resources(x['oil'], x['ammo'], x['steel'], x['aluminium'])

    # ================================
    # Combat
    # TODO: hardcoding A1, B1...
    # ================================

    '''
    def E6_1_A1_sortie(self) -> str:
        self.helper.api_withdraw()
        next_node_id = self.helper.api_readyFire()
        self.helper.api_newNext(str(next_node_id))

        shop_data = self.helper.get_ship_store()
        buy_data = self.helper.buy_ships(self.escort_DD, shop_data)
        self.set_boat_pool(buy_data['boatPool'])
        self.set_fleets(buy_data['boatPool'])
        self.helper.set_war_fleets(self.battle_fleet)

        # Node E6-1 A1, lv.1 -> lv.2
        adj_data = self.helper.cast_skill()
        if self.helper.bump_level(adj_data) is False:
            self.logger.info('Bumping failed. Should restart current sub-map.')
        else:
            pass

        sp_res = self.helper.supply_boats(self.battle_fleet)
        self.set_side_dock_resources(sp_res['userVo'])

        repair_res = self.helper.process_repair(sp_res['shipVO'], [self.repair_level])  # pre-battle repair
        self.set_side_dock_resources(repair_res['userVo'])
        set_sleep()
        self.helper.spy()
        set_sleep()
        challenge_res = self.helper.challenge(formation='1')
        do_night_battle = self.helper.is_night_battle(challenge_res)
        set_sleep(level=2)
        if do_night_battle is True:
            battle_res = self.helper.get_war_result('1')
        else:
            battle_res = self.helper.get_war_result('0')
        self.helper.process_battle_result(battle_res, self.battle_fleet)
        set_sleep()
        repair_res = self.helper.process_repair(battle_res['shipVO'], [self.repair_level])  # post-battle repair
        self.set_side_dock_resources(repair_res['userVo'])
        if int(battle_res['getScore$return']['flagKill']) == 1 or battle_res['resultLevel'] in [1, 2]:  # TODO: changes to < 5
            next_id = self.helper.get_next_node_by_id(battle_res['nodeInfo']['node_id'])
        else:
            self.logger.info('Failed to clean E6-1 A1. Should restart. Exiting.')
            next_id = -1
        return next_id

    def E6_1_B1_sortie(self, curr_id: str) -> str:
        self.helper.api_newNext(str(curr_id))
        shop_data = self.helper.get_ship_store()
        buy_data = self.helper.buy_ships(self.escort_CV, shop_data)
        self.set_boat_pool(buy_data['boatPool'])
        self.set_fleets(buy_data['boatPool'])
        self.helper.set_war_fleets(self.battle_fleet)

        sp_res = self.helper.supply_boats(self.battle_fleet)
        self.set_side_dock_resources(sp_res['userVo'])

        repair_res = self.helper.process_repair(sp_res['shipVO'], [self.repair_level])  # pre-battle repair
        self.set_side_dock_resources(repair_res['userVo'])
        set_sleep()
        self.helper.spy()
        set_sleep()
        challenge_res = self.helper.challenge(formation='1')
        do_night_battle = self.helper.is_night_battle(challenge_res)
        set_sleep(level=2)
        if do_night_battle is True:
            self.logger.info("Entering night war...")
            battle_res = self.helper.get_war_result('1')
        else:
            self.logger.info("")
            battle_res = self.helper.get_war_result('0')
        self.helper.process_battle_result(battle_res, self.battle_fleet)
        set_sleep()
        repair_res = self.helper.process_repair(battle_res['shipVO'], [self.repair_level])  # post-battle repair
        self.set_side_dock_resources(repair_res['userVo'])
        if int(battle_res['getScore$return']['flagKill']) == 1 or battle_res['resultLevel'] < 5:
            next_id = str(self.helper.get_next_node_by_id(battle_res['nodeInfo']['node_id']))
        else:
            self.logger.info('Failed to clean E6-1 B1. Should restart. Exiting.')
            next_id = "0"
        return next_id
    '''

    def E6A1(self) -> str:
        self.helper.api_withdraw()
        next_node_id = self.helper.api_readyFire()
        self.single_node_sortie(next_node_id)

    def find_SS(self, shop_data: list) -> list:
        # Get from a list of int (max length of 5), return a list of ship_id (str)
        res = []
        for ship_id in shop_data:
            if ship_id in self.main_fleet:
                res.append(str(ship_id))
        return res

    def single_node_sortie(self, curr_node_id: str) -> str:
        self.helper.api_newNext(str(curr_node_id))

        buy_res = None
        if curr_node_id == '931602':
            shop_res = self.helper.get_ship_store()
            buy_res = self.helper.buy_ships(self.escort_DD, shop_res)
        elif curr_node_id == '931604':
            shop_res = self.helper.get_ship_store()
            buy_res = self.helper.buy_ships(self.escort_CV, shop_res)
        # elif curr_node_id == '931607':
        #     # TODO: find COST 4 SS
        #     shop_res = self.helper.get_ship_store()
        #     shop_res['boats']
        #     buy_res = self.helper.buy_ships(['132974'], shop_res)
        else:
            # TODO: buy SS
            shop_res = self.helper.get_ship_store()
            ss_lists = self.find_SS(shop_res['boats'])
            if len(ss_lists) == 0:
                shop_res = self.helper.get_ship_store('1')
                ss_lists = self.find_SS(shop_res['boats'])
                if len(ss_lists) == 0:
                    pass
                else:
                    buy_res = self.helper.buy_ships(ss_lists, shop_res)
            else:
                buy_res = self.helper.buy_ships(ss_lists, shop_res)

        if buy_res is None:
            pass
        else:
            self.set_boat_pool(buy_res['boatPool'])
            # TODO: when SS count >= 4, set all to SS, done?
            self.set_fleets(buy_res['boatPool'])
            # TODO: when final fleet elem == battle_fleet elem; skip set-war-fleet
            if set(self.battle_fleet) == set(self.final_fleet):
                # skip
                pass
            else:
                self.helper.set_war_fleets(self.battle_fleet)

        # cast skill
        if curr_node_id in ['931602', '931702']:
            adj_res = self.helper.cast_skill()
            self.helper.set_adjutant_info(adj_res)
        elif curr_node_id == '931802':
            # TODO habakkuk; maybe not here
            pass
        else:
            pass

        if self.helper.can_bump() is True:
            if (adj_res is not None) and (self.helper.bump_level(adj_res) is False):
                self.logger.info('Bumping failed. Should restart current sub-map.')
            else:
                pass
        else:
            pass

        set_sleep()
        supply_res = self.helper.supply_boats(self.battle_fleet)
        self.set_side_dock_resources(supply_res['userVo'])

        repair_res = self.helper.process_repair(supply_res['shipVO'], [self.repair_level])  # pre-battle repair
        self.set_side_dock_resources(repair_res['userVo'])

        set_sleep()
        self.helper.spy()

        set_sleep()
        challenge_res = self.helper.challenge(formation='1')


        do_night_battle = self.helper.is_night_battle(curr_node_id, challenge_res)

        set_sleep(level=2)
        if do_night_battle is True:
            self.logger.info("Entering night war...")
            battle_res = self.helper.get_war_result('1')
        else:
            self.logger.info("")
            battle_res = self.helper.get_war_result('0')
        self.helper.process_battle_result(battle_res, self.battle_fleet)

        set_sleep()
        repair_res = self.helper.process_repair(battle_res['shipVO'], [self.repair_level])  # post-battle repair
        self.set_side_dock_resources(repair_res['userVo'])

        if int(battle_res['getScore$return']['flagKill']) == 1 or battle_res['resultLevel'] < 5:
            next_id = str(self.helper.get_next_node_by_id(battle_res['nodeInfo']['node_id']))
        else:
            self.logger.info('Failed to clean E6-1 B1. Should restart. Exiting.')
            next_id = "0"
        return next_id

# End of File
