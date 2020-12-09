from logging import getLogger
from math import ceil
from typing import Callable, Tuple

from src import utils as wgv_utils
from src.exceptions.wgr_error import get_error, WarshipGirlsExceptions
from src.exceptions.custom import ThermopylaeSoriteExit
from src.wgr.six import API_SIX  # only for typehints

ADJUTANT_ID_TO_NAME = {
    '10082': "紫貂",
    '10182': "Kearsarge",
    '10282': "Habakkuk"
}


class SortieHelper:
    def __init__(self, tab_thermopylae, api: API_SIX, user_ships: dict, map_data: dict):
        self.api = api
        self.tab_thermopylae = tab_thermopylae
        self.logger = getLogger('TabThermopylae')
        self.user_ships = user_ships
        self.map_data = map_data

        self.max_retry = 3
        self.points = -1
        self.init_sub_map = "9316"  # TODO

        self.logger.debug('SortieHelper is initiated')

    def _reconnecting_calls(self, func: Callable, func_info: str) -> [dict, object]:
        # This redundancy while-loop (compared to api.py's while-loop) deals with WarshipGirlsExceptions;
        #   while the other one deals with URLError etc
        res = False  # status
        data = None
        tries = 0
        while not res:
            try:
                self.logger.info(f"{func_info}...")
                res, data = func()
            except WarshipGirlsExceptions as e:
                self.logger.warning(f'Failed to {func_info} due to {e}')
                self.logger.warning('Trying reconnecting...')
                wgv_utils.set_sleep()

            tries += 1
            if tries >= self.max_retry:
                self.logger.error(f"Failed to {func_info} after {self.max_retry} reconnections. Please try again later.")
                raise ThermopylaeSoriteExit()
            else:
                pass
        return data

    # ================================================================
    # WGR API methods
    # Every API calls has at least 3 results:
    #   - fail;    WGR 'eid' response
    #   - success; check for specific field names
    #   - unknown; unexpected
    # ================================================================

    def api_withdraw(self) -> dict:
        def _withdraw() -> Tuple[bool, dict]:
            data = self.api.withdraw()
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif 'getLevelList' in data:
                self.logger.info("Retreat success. Fresh start is ready.")
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        return self._reconnecting_calls(_withdraw, 'restart')

    def api_readyFire(self) -> dict:
        def _readyFire() -> Tuple[bool, int]:
            data = self.api.readyFire(self.init_sub_map)
            if 'eid' in data:
                get_error(data['eid'])
                next_node_id = -1
                res = False
            elif '$currentVo' in data:
                self.logger.info('Entering map succeed!')
                next_node_id, _ = self.get_next_node_by_id(data['$currentVo']['nodeId'])
                res = True
            else:
                self.logger.debug(data)
                next_node_id = -1
                res = False
            return res, next_node_id

        return self._reconnecting_calls(_readyFire, 'enter the map')

    def api_newNext(self, next_node: str) -> dict:
        def _newNext() -> Tuple[bool, dict]:
            data = self.api.newNext(next_node)
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif 'nodeId' in data:
                _, node_name = self.get_next_node_by_id(next_node)
                self.logger.info(f"Proceed to {node_name} succeed!")
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        return self._reconnecting_calls(_newNext, 'enter next node')

    def get_ship_store(self, is_refresh: str = '0') -> dict:
        def _canSelectList() -> Tuple[bool, dict]:
            data = self.api.canSelectList(is_refresh)
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif '$ssss' in data:
                self.logger.info('Visiting shop succeed!')
                res = True
            else:
                self.logger.error(data)
                res = False
            return res, data

        store_data = self._reconnecting_calls(_canSelectList, 'visit shop')
        # TODO: delete
        self.logger.info('Shop has following: ')
        for ship in store_data['$ssss']:
            output_str = f'{self.user_ships[str(ship[1])]["Name"]} - LV {ship[0]} - COST {ship[2]}'
            self.logger.info(output_str)
            # TODO: where is buff card? (low priority)
        return store_data

    def buy_ships(self, purchase_list: list, shop_data: dict):
        def _selectBoat() -> [bool, object]:
            data = self.api.selectBoat(purchase_list)
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.info("Buying ships failed...")
                res = False
            elif 'boatPool' in data:
                self.logger.info("Buying ships successfully!")
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        buy_data = self._reconnecting_calls(_selectBoat, 'buy ships')

        # calculate remaining points
        self.points = shop_data['strategic_point']
        for ship in shop_data['$ssss']:
            if ship[1] in purchase_list:
                self.logger.info(f'bought {self.user_ships[str(ship[1])]["Name"]}')
                self.points -= int(ship[2])
        return buy_data

    def buy_exp(self) -> dict:
        def _buy_exp() -> Tuple[bool, dict]:
            data = self.api.adjutantExp()
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif 'adjutantData' in data:
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        return self._reconnecting_calls(_buy_exp, 'buy exp')

    def cast_skill(self) -> dict:
        def _cast_skill() -> Tuple[bool, dict]:
            data = self.api.useAdjutant()
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.info("Failed to cast adjutant skill...")
                res = False
            elif 'adjutantData' in data:
                self.logger.info("Adjutant skill casted successfully!")
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        res_data = self._reconnecting_calls(_cast_skill, 'cast adjutant skill')

        self.update_adjutant_info(res_data['adjutantData'], res_data['strategic_point'])
        return res_data

    def set_war_fleets(self, fleets: list) -> dict:
        def _set_fleets() -> Tuple[bool, dict]:
            data = self.api.setWarFleet(fleets)
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif 'fleet' in data and len(data['fleet']) > 0:
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        res_data = self._reconnecting_calls(_set_fleets, 'set battle fleet')
        return res_data

    def supply_boats(self, fleets: list) -> dict:
        def _supply_boats() -> Tuple[bool, dict]:
            data = self.api.supplyBoats(fleets)
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.info("Supply ships failed...")
                res = False
            elif 'userVo' in data:
                self.logger.info("Supply boats successfully!")
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        return self._reconnecting_calls(_supply_boats, 'supply')

    def repair(self, fleets: list) -> dict:
        def _repair() -> Tuple[bool, dict]:
            data = self.api.instantRepairShips(fleets)
            print(data)
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.info(f"Failed to repair {fleets}")
                res = False
                # TODO elif
            else:
                res = True
            return res, data

        return self._reconnecting_calls(_repair, 'repair')

    def spy(self) -> dict:
        def _spy() -> Tuple[bool, dict]:
            data = self.api.spy()
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif 'enemyVO' in data:
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        return self._reconnecting_calls(_spy, 'Detection')

    def challenge(self, formation: str) -> dict:
        def _challenge() -> Tuple[bool, dict]:
            data = self.api.challenge(formation)
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif 'warReport' in data:
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        return self._reconnecting_calls(_challenge, 'Combat')

    def get_war_result(self, is_night: str = '0') -> dict:
        def _result() -> Tuple[bool, dict]:
            data = self.api.getWarResult(is_night)
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif 'warResult' in data:
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data

        return self._reconnecting_calls(_result, 'receive result')

    # ================================
    # Non-WGR methods
    # ================================

    def get_curr_points(self) -> int:
        return self.points

    def get_map_node_by_id(self, node_id: str) -> dict:
        try:
            node = next(i for i in self.map_data['combatLevelNode'] if i['id'] == node_id)
        except StopIteration:
            self.logger.error('Access wrong nodes.')
            node = {}
        return node

    def get_next_node_by_id(self, node_id: str) -> Tuple[str, str]:
        try:
            next_node = self.get_map_node_by_id(node_id)
            next_node_id = str(next_node['next_node'][0])
            next_node_name = self.get_map_node_by_id(next_node_id)['flag']
        except KeyError:
            self.logger.error('Access wrong nodes.')
            next_node_id = ""
            next_node_name = "??"
        print(next_node_id, next_node_name)
        return next_node_id, next_node_name

    def bump_level(self, adj_data) -> bool:
        adj_lvl = int(adj_data["adjutantData"]["level"])
        next_adj_lvl = adj_lvl + 1
        curr_exp = int(adj_data["adjutantData"]["exp"])
        next_exp = int(adj_data["adjutantData"]["exp_top"])
        required_exp = next_exp - curr_exp
        if self.get_curr_points() >= required_exp:
            self.logger.info(f"Bumping adjutant level to Lv.{next_adj_lvl}")
            buy_times = ceil(required_exp / 5)
            res = None
            while buy_times > 0:
                res = self.buy_exp()
                buy_times -= 1
                if buy_times < 0:
                    break
                self.update_adjutant_info(res['adjutantData'], res['strategic_point'])
                wgv_utils.set_sleep()
            if res is None:
                return False
            elif int(res['adjutantData']['level']) == next_adj_lvl:
                self.logger.info("Bumping level successfully")
                return True
            else:
                self.logger.debug(res)
                return False
        else:
            return False

    def update_adjutant_info(self, adj_data, strategic_point):
        # TODO: use signal? and manage signals globally?
        _name = ADJUTANT_ID_TO_NAME[adj_data['id']]
        _exp = f"Lv. {adj_data['level']} {adj_data['exp']}/{adj_data['exp_top']}"
        _point = str(strategic_point)
        self.points = strategic_point
        self.tab_thermopylae.update_adjutant_name(_name)
        self.tab_thermopylae.update_adjutant_exp(_exp)
        self.tab_thermopylae.update_points(_point)

    def process_repair(self, ships: list, repair_levels: [int, list]) -> None:
        repairs = []
        ship_ids = []
        for ship in ships:
            repairs.append(wgv_utils.get_repair_type(ship))
            ship_ids.append(ship['id'])

        if isinstance(repair_levels, int):
            # all ships share the same repair scheme
            repair_levels = [repair_levels] * len(ships)
        elif isinstance(repair_levels, list) and len(repair_levels) > 0:
            try:
                assert len(ships) == len(repair_levels)
                repair_levels = repair_levels
            except AssertionError:
                repair_levels = [repair_levels[0]] * len(ships)
        else:
            # default repair all moderately damaged ships
            repair_levels = [1] * len(ships)

        to_repair = []
        for i in range(len(ships)):
            if repairs[i] >= repair_levels[i]:
                to_repair.append(ship_ids[i])
            else:
                pass
        if len(to_repair) > 0:
            self.repair(to_repair)
        else:
            pass

    def is_night_battle(self, challenge_res: dict) -> bool:
        if challenge_res['warReport']['canDoNightWar'] == 0:
            self.logger.info('Battle finished by day')
            do_night_battle = False
        elif challenge_res['warReport']['canDoNightWar'] == 1:
            e_list = challenge_res['warReport']['hpBeforeNightWarEnemy']
            self.logger.info(e_list)
            if e_list[0] != 0:  # if enemy's flagship is sunken
                do_night_battle = True
            else:
                do_night_battle = False
        else:
            self.logger.info("Cannot process battle info. Exiting")
            do_night_battle = False
        return do_night_battle

    def process_battle_result(self, battle_res: dict):
        res_str = f"==== {wgv_utils.get_war_evaluation(battle_res['resultLevel'])} ===="
        self.logger.info(res_str)
        self.update_adjutant_info(battle_res['adjutantData'], battle_res['strategic_point'])

        ships = battle_res['warResult']['selfShipResults']
        for i in range(len(ships)):
            shipname = battle_res['shipVO'][i]['title']
            ship = ships[i]
            ship_str = f"{shipname} Lv.{ship['level']} +{ship['expAdd']}Exp"
            ship_str += " MVP" if ship['isMvp'] == 1 else ""
            self.logger.info(ship_str)

# End of File
