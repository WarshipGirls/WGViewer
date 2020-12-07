from time import sleep
from typing import Callable
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
        self.logger.debug('SortieHelper is initiated')

    def is_exit(self):
        return self.force_exit

    def _reconnecting_calls(self, func: Callable, func_info: str):
        # This redundancy while-loop (compared to api.py's while-loop) deals with WarshipGirlsExceptions;
        #   while the other one deals with URLError etc
        res = [False, None]  # status, data
        tries = 0
        while not res[0]:
            try:
                self.logger.info(f"{func_info}...")
                res = func()
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
        return res[1]

    # ================================
    # WGR API methods
    # ================================

    def api_withdraw(self):
        def _withdraw() -> list:
            data = self.api.withdraw()
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            elif data is not None:
                self.logger.info("Retreat success. Fresh start is ready.")
                res = True
            else:
                self.logger.error('Unexpected behavior')
                self.logger.debug(data)
                res = False
            return [res, data]

        return self._reconnecting_calls(_withdraw, 'restart')

    def api_readyFire(self):
        def _readyFire() -> list:
            data = self.api.readyFire(self.init_sub_map)
            if 'eid' in data:
                get_error(data['eid'])
                next_node_id = -1
                res = False
            else:
                self.logger.info('Entering map succeed!')
                next_node = self.get_map_node(data['$currentVo']['nodeId'])
                # Always choose the upper path
                next_node_id = next_node['next_node'][0]
                res = True
            return [res, next_node_id]

        return self._reconnecting_calls(_readyFire, 'enter the map')

    def api_newNext(self, next_node: str):
        def _newNext() -> list:
            # get 11009211 and 11008211
            data = self.api.newNext(next_node)
            if 'eid' in data:
                get_error(data['eid'])
                res = False
            else:
                _flag = self.get_map_node(next_node)['flag']
                self.logger.info(f"Proceed to {_flag} succeed!")
                res = True
            return [res, data]

        return self._reconnecting_calls(_newNext, 'enter next node')

    def get_ship_store(self, is_refresh: str = '0'):
        def _canSelectList() -> list:
            data = self.api.canSelectList(is_refresh)
            if '$ssss' in data:
                self.logger.info('Visiting shop succeed!')
                res = True
            elif 'eid' in data:
                get_error(data['eid'])
                res = False
            elif data is None:
                self.logger.info("Cannot visit shop")
                res = False
            else:
                self.logger.error('Unexpected behavior')
                res = False
            return [res, data]

        store_data = self._reconnecting_calls(_canSelectList, 'visit shop')
        print(store_data)
        self.logger.info('Shop has following: ')
        for ship in store_data['$ssss']:
            output_str = f'{self.user_ships[str(ship[1])]["Name"]} - LV {ship[0]} - COST {ship[2]}'
            self.logger.info(output_str)
            # TODO: where is buff card? (low priority)
        return store_data

    def buy_ships(self, purchase_list: list, shop_data: dict):
        def _selectBoat() -> list:
            # TODO TODO can't tell if this is success or not due to urlopen response encoding
            data = self.api.selectBoat(purchase_list)
            if len(data) < 25:  # workaround
                res = False
            else:
                res = True
            return [res, data]
        self._reconnecting_calls(_selectBoat, 'buy ships')

        # calculate remaining points
        self.points = shop_data['strategic_point']
        for ship in shop_data['$ssss']:
            if ship[1] in purchase_list:
                self.logger.info(f'bought {self.user_ships[str(ship[1])]["Name"]}')
                self.points -= int(ship[2])
        self.get_curr_points()

    # ================================
    # Non-WGR methods
    # ================================

    def get_curr_points(self) -> int:
        self.logger.info(f'Now have {self.points} strategic points left.')
        return self.points

    def get_map_node(self, node_id: str) -> dict:
        try:
            node = next(i for i in self.map_data['combatLevelNode'] if i['id'] == node_id)
        except StopIteration:
            self.logger.error('Access wrong nodes.')
            node = {}
        return node

# End of File
