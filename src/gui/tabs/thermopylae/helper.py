from time import sleep
from typing import Callable, Tuple
from logging import getLogger

from src.wgr.api import WGR_API  # only for typehints
from src.exceptions.wgr_error import get_error, WarshipGirlsExceptions


class SortieHelper:
    def __init__(self, api: WGR_API, user_ships: dict, map_data: dict):
        self.api = api
        self.logger = getLogger('TabThermopylae')
        self.user_ships = user_ships
        self.map_data = map_data

        self.sleep_time = 7
        self.max_retry = 5
        self.points = -1
        self.init_sub_map = "9316"  # TODO
        self.force_exit = False
        self.adjutant_name = {
            '10082': "紫貂",
            '10182': "Kearsarge",
            '10282': "Habakkuk"
        }
        self.logger.debug('SortieHelper is initiated')

    def is_exit(self):
        return self.force_exit

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
                sleep(self.sleep_time)

            tries += 1
            if tries >= self.max_retry:
                self.logger.error(f"Failed to {func_info} after {self.max_retry} reconnections. Please try again later.")
                self.force_exit = True
                break
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
                next_node = self.get_map_node(data['$currentVo']['nodeId'])
                # Always choose the upper path
                next_node_id = next_node['next_node'][0]
                res = True
            else:
                self.logger.debug(data)
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
                _flag = self.get_map_node(next_node)['flag']
                self.logger.info(f"Proceed to {_flag} succeed!")
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
        self.get_curr_points()
        return buy_data

    def buy_exp(self) -> dict:
        def _buy_exp() -> Tuple[bool, dict]:
            data = self.api.adjutantExp()
            if 'eid' in data:
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

        self.points = res_data['strategic_point']
        adj = res_data['adjutantData']
        output_str = f'{self.adjutant_name[adj["id"]]} - Lv.{adj["level"]} {adj["exp"]}/{adj["exp_top"]}'
        self.logger.info(output_str)
        self.get_curr_points()
        return res_data

    def set_sortie_fleets(self, fleets: list) -> dict:
        def _set_fleets() -> Tuple[bool, dict]:
            data = self.api.setWarFleet(fleets)
            if 'eid' in data:
                res = False
            elif 'fleet' in data:
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data
        res_data = self._reconnecting_calls(_set_fleets, 'settings fleet')
        return res_data

    def supply_boats(self, fleets: list) -> object:
        def _supply_boats() -> Tuple[bool, dict]:
            data = self.api.supplyBoats(fleets)
            if 'eid' in data:
                self.logger.info("Supply boat failed...")
                res = False
            elif 'userVo' in data:
                self.logger.info("Supply boat successfully!")
                res = True
            else:
                self.logger.debug(data)
                res = False
            return res, data
        return self._reconnecting_calls(_supply_boats, 'supply')

    # ================================
    # Non-WGR methods
    # ================================

    def get_curr_points(self, is_print: bool = True) -> int:
        # TODO break apart
        if is_print is True:
            self.logger.info(f'Now have {self.points} strategic points left.')
        else:
            pass
        return self.points

    def get_map_node(self, node_id: str) -> dict:
        try:
            node = next(i for i in self.map_data['combatLevelNode'] if i['id'] == node_id)
        except StopIteration:
            self.logger.error('Access wrong nodes.')
            node = {}
        return node

# End of File
