from math import ceil
from typing import Callable, Tuple

from PyQt5.QtCore import QSettings

from src import utils as wgv_utils
from src.data import get_qsettings_file
from src.func import qsettings_keys as QKEYS
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from src.exceptions.wgr_error import get_error, WarshipGirlsExceptions
from src.exceptions.custom import ThermopylaeSortieExit, ThermopylaeSortieResume
from src.wgr import API_SIX
from . import constants as T_CONST


class SortieHelper:
    def __init__(self, tab_thermopylae, api: API_SIX, user_ships: dict, map_data: dict):
        self.api = api
        self.tab_thermopylae = tab_thermopylae
        self.logger = get_logger(QLOGS.TAB_THER)
        self.user_ships = user_ships
        self.map_data = map_data

        self.qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
        if self.qsettings.contains(QKEYS.CONN_THER_RTY):
            self.reconnection_limit = self.qsettings.value(QKEYS.CONN_THER_RTY, type=int)
        else:
            self.reconnection_limit = 3
        if self.qsettings.contains(QKEYS.THER_BOSS_RTY):
            self.boss_retry_limit = list(map(int, self.qsettings.value(QKEYS.THER_BOSS_RTY)))
        else:
            self.boss_retry_limit = [3, 5, 10]
        if self.qsettings.contains(QKEYS.THER_BOSS_STD):
            self.boss_retry_standard = list(map(int, self.qsettings.value(QKEYS.THER_BOSS_STD)))
        else:
            self.boss_retry_standard = [1, 2, 2]
        if self.qsettings.contains(QKEYS.THER_SHIP_STARS):
            self.ship_star: dict = self.qsettings.value(QKEYS.THER_SHIP_STARS)
        else:
            self.ship_star: dict = {}

        self.boss_retry_count: list = [0, 0, 0]
        self.points: int = 10
        self.adjutant_info: dict = {}  # level, curr_exp, exp_cap

    def _reconnecting_calls(self, func: Callable, func_info: str) -> [dict, object]:
        # This redundancy while-loop (compared to api.py's while-loop) deals with WarshipGirlsExceptions;
        #   while the other one deals with URLError etc
        res = False  # status
        data = None
        tries = 0
        while not res:
            try:
                self.logger.debug(f"{func_info}...")
                res, data = func()
            except WarshipGirlsExceptions as e:
                self.logger.warning(f"Failed to {func_info} due to {e}. Trying reconnecting...")
                wgv_utils.set_sleep()
            tries += 1
            if tries >= self.reconnection_limit:
                raise ThermopylaeSortieExit(f"Failed to {func_info} after {self.reconnection_limit} reconnections")
            else:
                pass
        return data

    # ================================================================
    # WGR API Combat Methods
    # Every API calls has at least 3 results:
    #   - fail;    WGR 'eid' response
    #   - success; check for specific field names
    #   - unknown; unexpected
    # ================================================================

    def buy_exp(self) -> dict:
        def _buy_exp() -> Tuple[bool, dict]:
            data = self.api.adjutantExp()
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'adjutantData' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_buy_exp, 'buy exp')

    def buy_ships(self, purchase_list: list, shop_data: dict = None, buff_card: str = '0') -> dict:
        purchase_list = list(set(purchase_list))

        def _selectBoat() -> [bool, object]:
            data = self.api.selectBoat(purchase_list, buff_card)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.warning("Buying ships failed...")
            elif 'boatPool' in data:
                self.logger.info("Buying ships successfully!")
                res = True
            else:
                self.logger.debug(data)
            return res, data

        self.logger.debug('prepare to buy')
        self.logger.debug(purchase_list)
        buy_data = self._reconnecting_calls(_selectBoat, 'buy ships')

        if 'strategic_point' in buy_data and shop_data is not None:
            self.set_curr_points(buy_data['strategic_point'])
            for s in purchase_list:
                if str(s) in self.ship_star:
                    self.ship_star[str(s)] += 1
                else:
                    self.ship_star[str(s)] = 0
                self.logger.info(f'bought {self.user_ships[str(s)]["Name"]}')
            self.qsettings.setValue(QKEYS.THER_SHIP_STARS, self.ship_star)
        else:
            pass

        return buy_data

    def cast_skill(self) -> dict:
        def _cast_skill() -> Tuple[bool, dict]:
            data = self.api.useAdjutant()
            res = False
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.warning("Failed to cast adjutant skill...")
            elif 'adjutantData' in data:
                self.logger.info("Adjutant skill casted successfully!")
                res = True
            else:
                self.logger.debug(data)
            return res, data

        res_data = self._reconnecting_calls(_cast_skill, 'cast adjutant skill')

        if res_data['adjutantData']['id'] == T_CONST.ADJUTANT_IDS[0]:
            self.update_adjutant_info(res_data['adjutantData'], res_data['strategic_point'])
        elif res_data['adjutantData']['id'] == T_CONST.ADJUTANT_IDS[2]:
            self.update_adjutant_info(res_data['adjutantData'], self.get_curr_points())
        else:
            pass
        return res_data

    def challenge(self, formation: str) -> dict:
        def _challenge() -> Tuple[bool, dict]:
            data = self.api.challenge(formation)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'warReport' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_challenge, 'Combat')

    def charge_ticket(self, resource_typd_id: str) -> dict:
        def _buy() -> Tuple[bool, dict]:
            data = self.api.chargeTicket(resource=resource_typd_id)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'userResVO' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_buy, 'buy ticket')

    def enter_next_node(self, next_node: str) -> dict:
        def _newNext() -> Tuple[bool, dict]:
            data = self.api.newNext(next_node)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'nodeId' in data:
                node_name = self.get_map_node_by_id(next_node)['flag']
                self.logger.info(f"Proceed to {node_name} succeed!")
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_newNext, 'enter next node')

    def get_ship_store(self, is_refresh: str = '0') -> dict:
        def _canSelectList() -> Tuple[bool, dict]:
            data = self.api.canSelectList(is_refresh)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif '$ssss' in data:
                self.logger.info('Visiting shop succeed!')
                res = True
            elif 'hadResetSelectFlag' in data:
                res = True
            else:
                self.logger.error(data)
            return res, data

        store_data = self._reconnecting_calls(_canSelectList, 'visit shop')
        if '$ssss' not in store_data:
            return store_data
        self.set_curr_points(store_data['strategic_point'])
        # notes that the server only return affordable ships and buff
        # since CN ver 5.1.0, there are only 4 ships + 1 buff
        self.logger.info('Affordable ships: ')
        for ship in store_data['$ssss']:
            star = int(ship[0])
            cost = int(ship[2]) * (2 ** (star - 1))
            output_str = "{:15s}\tSTAR{:3s} COST{:4s}".format(self.user_ships[str(ship[1])]["Name"], str(star-1), str(cost))
            self.logger.info(output_str)
        return store_data

    def get_war_result(self, is_night: str = '0') -> dict:
        if is_night == '1':
            self.logger.info("Fighting night battle")
        else:
            pass

        def _result() -> Tuple[bool, dict]:
            data = self.api.getWarResult(is_night)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'warResult' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_result, 'receive result')

    def repair_ships(self, fleet: list) -> dict:
        def _repair() -> Tuple[bool, dict]:
            data = self.api.instantRepairShips(fleet)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.warning(f"Failed to repair {fleet}")
            elif 'shipVOs' in data:
                self.logger.info("Repaired successfully")
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_repair, 'repair')

    def scout_enemy(self) -> dict:
        def _spy() -> Tuple[bool, dict]:
            data = self.api.spy()
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'enemyVO' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_spy, 'Detection')

    def set_chapter_fleet(self, chapter_map: str, fleet: list) -> dict:
        def _set_fleets() -> Tuple[bool, dict]:
            data = self.api.setChapterBoat(chapter_map, fleet)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'chapterInfo' in data and 'boats' in data['chapterInfo']:
                if len(set(fleet).difference(set(data['chapterInfo']['boats']))) == 0:
                    res = True
                else:
                    self.logger.debug('undesired chapter ship set')
                    self.logger.debug(data)
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_set_fleets, 'set chapter boats')

    def set_war_fleet(self, fleet: list) -> dict:
        def _set_fleets() -> Tuple[bool, dict]:
            data = self.api.setWarFleet(fleet)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'fleet' in data and len(data['fleet']) > 0:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_set_fleets, 'set battle fleet')

    def supply_boats(self, fleet: list) -> dict:
        def _supply_boats() -> Tuple[bool, dict]:
            data = self.api.supplyBoats(fleet)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
                self.logger.warning("Supply ships failed...")
            elif 'userVo' in data:
                self.logger.info("Supply boats successfully!")
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_supply_boats, 'supply')

    # ================================
    # WGR API Map Methods
    # ================================

    def reset_chapter(self, chapter_id: str) -> dict:
        def _reset() -> Tuple[bool, dict]:
            data = self.api.resetChapter(chapter_id)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'adjutantData' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_reset, 'reset chapter')

    def enter_sub_map(self, sub_map_id: str) -> dict:
        def _readyFire() -> Tuple[bool, int]:
            data = self.api.readyFire(sub_map_id)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
                next_node_id = -1
            elif '$currentVo' in data:
                self.logger.info('Entering map succeed!')
                next_node_id = self.get_next_node_by_id(data['$currentVo']['nodeId'])
                res = True
            else:
                self.logger.debug(data)
                next_node_id = -1
            return res, next_node_id

        return self._reconnecting_calls(_readyFire, 'enter the map')

    def retreat_sub_map(self) -> dict:
        def _withdraw() -> Tuple[bool, dict]:
            data = self.api.withdraw()
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'code' in data:
                get_error(data['code'])
            elif 'getLevelList' in data:
                self.logger.info("Retreat success. Fresh start is ready.")
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_withdraw, 'restart')

    def pass_sub_map(self) -> dict:
        def _pass() -> Tuple[bool, dict]:
            data = self.api.passLevel()
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'code' in data:
                get_error(data['code'])
            elif 'attach' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_pass, 'collect boss reward')

    # ================================================================
    # Getter / Setter
    # ================================================================

    def get_adjutant_info(self) -> dict:
        return self.adjutant_info

    @staticmethod
    def get_buff_card_cost(buff_id: str) -> int:
        try:
            assert (len(buff_id) == 6)
            cost = T_CONST.BUFF_BASE_COST[int(buff_id[:4])] * (2 ** (int(buff_id[-2:]) - 1))
            return cost
        except AssertionError:
            return -1

    @staticmethod
    def get_challenge_formation(curr_node_id: str, battle_fleet_size: int) -> str:
        if curr_node_id in ['931608', '931610']:  # only these two nodes need anti-sub
            formation = '5'
        elif curr_node_id in T_CONST.REWARD_NODES or curr_node_id in T_CONST.BOSS_NODES:
            formation = '4'
        elif battle_fleet_size >= 4:
            formation = '2'
        else:
            formation = '1'
        return formation

    def get_curr_points(self) -> int:
        return self.points

    def get_map_node_by_id(self, node_id: str) -> dict:
        try:
            node = next(i for i in self.map_data['combatLevelNode'] if i['id'] == str(node_id))
        except StopIteration:
            self.logger.debug(node_id)
            self.logger.error('Access wrong nodes.')
            node = {}
        return node

    def get_next_node_by_id(self, node_id: str) -> str:
        self.logger.debug(f'Get next for {node_id}')
        try:
            next_node = self.get_map_node_by_id(node_id)
            if len(next_node['next_node']) == 0:
                next_node_id = ""  # Boss node
            else:
                next_node_id = str(next_node['next_node'][0])
        except KeyError:
            self.logger.error('Access wrong nodes.')
            next_node_id = "-1"
        return next_node_id

    def set_adjutant_info(self, adj_data: dict) -> None:
        self.logger.debug(adj_data)
        self.adjutant_info = adj_data

    def set_curr_points(self, points) -> None:
        self.logger.debug(f"{self.points} -> {points}")
        self.points = points
        self.tab_thermopylae.update_points(self.points)

    # ================================================================
    # Assistant methods
    # ================================================================

    def bump_level(self) -> int:
        if self.adjutant_info is None:
            return -1

        adj_lvl = int(self.adjutant_info['level'])
        if adj_lvl == 10:
            return 1

        curr_exp = int(self.adjutant_info["exp"])
        next_exp = int(self.adjutant_info["exp_top"])
        required_exp = next_exp - curr_exp
        required_points = ceil(required_exp / 5) * 5
        next_adj_lvl = adj_lvl + 1
        if self.get_curr_points() >= required_points:
            if adj_lvl >= 8 and required_points > 5:
                res = 0
            else:
                exp_res = None
                while required_points > 0:
                    exp_res = self.buy_exp()
                    required_points -= 5
                    self.update_adjutant_info(exp_res['adjutantData'], exp_res['strategic_point'])
                    wgv_utils.set_sleep()

                if exp_res is None:
                    res = -1
                elif 'adjutantData' not in exp_res:
                    res = -1
                elif int(exp_res['adjutantData']['level']) == next_adj_lvl:
                    self.logger.info("Bumping level successfully")
                    res = 0
                else:
                    self.logger.debug(exp_res)
                    res = -1
        else:
            res = 0
        return res

    def check_night_battle(self, curr_id: str, challenge_res: dict) -> str:
        """
        Determines whether to proceed night battle given current node and day battle result.

        @param curr_id: current node id
        @type curr_id: str
        @param challenge_res: server response data from six/cha11enge
        @type challenge_res: dict
        @return: the option of proceed night battle
            - '0': no night battle
            - '1': do night battle
        @rtype:
        """
        e_list = challenge_res['warReport']['hpBeforeNightWarEnemy']
        self.logger.info(f'Enemies HP: {e_list}')
        if challenge_res['warReport']['canDoNightWar'] == 0:
            res = '0'
        elif curr_id in T_CONST.BOSS_NODES:
            self.logger.info('---- BOSS BATTLE ----')
            node_idx = T_CONST.BOSS_NODES.index(curr_id)
            if e_list.count(0) >= self.boss_retry_standard[node_idx]:
                res = '1'
            else:
                if self.boss_retry_count[node_idx] == self.boss_retry_limit[node_idx]:
                    res = '1'
                else:
                    self.boss_retry_count[node_idx] += 1
                    raise ThermopylaeSortieResume(f"E6-{node_idx + 1} BOSS NEEDS RE-BATTLE")
        elif curr_id in T_CONST.REWARD_NODES:
            res = '1'
        elif challenge_res['warReport']['canDoNightWar'] == 1:
            # if enemy's flagship is sunken, then no night battle
            res = '0' if e_list[0] == 0 else '1'
        else:
            self.logger.info("Cannot process battle info; no night battle.")
            res = '0'
        return res

    def find_affordable_ships(self, purchase_list: list, shop_data: dict, is_buff: bool) -> Tuple[list, str]:
        if len(purchase_list) == 0:
            return [], '0'

        # If point is insufficient, buy from the least expensive to the most
        purchase_list = [int(i) for i in purchase_list]
        ship_id_to_price = {}
        for ship in purchase_list:
            price = shop_data['buyPointArr'][shop_data['boats'].index(ship)]
            ship_id_to_price[ship] = price
        # Sort by price
        sorted_list = dict(sorted(ship_id_to_price.items(), key=lambda i: i[1]))
        total = 0
        res = []
        for ship_id in sorted_list:
            total += sorted_list[ship_id]
            if total > self.get_curr_points():
                total -= sorted_list[ship_id]
                break
            else:
                res.append(ship_id)
        # Getting buff if meets conditions
        buff_id = '0'
        if (is_buff is True) and (shop_data['buff'] in T_CONST.WORTH_BUYING_BUFFS):
            buff_price = self.get_buff_card_cost(shop_data['buff'])
            total += buff_price
            if total <= self.get_curr_points():
                buff_id = str(shop_data['buff'])
            else:
                pass
        else:
            pass
        return res, buff_id

    def get_ship_star(self) -> dict:
        return self.ship_star

    @staticmethod
    def is_buy_buff(node_id: str) -> bool:
        try:
            assert (len(node_id) == 6)
            if node_id in T_CONST.SUB_MAP3_ID:
                res = True
            else:
                res = False
            return res
        except AssertionError:
            return False

    def process_repair(self, ships: list, repair_levels: [int, list]) -> dict:
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
            repair_levels = [2] * len(ships)

        to_repair = []
        for i in range(len(ships)):
            if repairs[i] >= repair_levels[i]:
                to_repair.append(ship_ids[i])
            else:
                pass
        if len(to_repair) > 0:
            names = [self.user_ships[str(i)]['Name'] for i in to_repair]
            self.logger.info(f'Start to repair {names}')
            res = self.repair_ships(to_repair)
        else:
            res = {}
        return res

    def process_battle_result(self, battle_res: dict, fleet: list):
        res_str = f"==== {wgv_utils.get_war_evaluation(battle_res['resultLevel'])} ===="
        self.logger.info(res_str)
        self.update_adjutant_info(battle_res['adjutantData'], battle_res['strategic_point'])

        ships = battle_res['warResult']['selfShipResults']
        for i in range(len(ships)):
            ship_id = fleet[i]
            try:
                shipname = next((j for j in battle_res['shipVO'] if j['id'] == ship_id))['title']
            except StopIteration:
                self.logger.debug("Discrepancy in battle result shipVO")
                break
            ship = ships[i]
            ship_str = "{:12s}\tLv.{:4s}\t+{}Exp".format(shipname, str(ship['level']), str(ship['expAdd']))
            ship_str += " MVP" if ship['isMvp'] == 1 else ""
            self.logger.info(ship_str)

    """
    def process_boss_reward_result(self, reward_res: dict) -> str:
        # TODO: fail due to stupid WGR developer's coding practice
        self.logger.info("######## BOSS REWARDS ########")
        replaced = str(reward_res).replace('False', '{}')
        json_obj = json.loads(replaced)
        rewards = json_obj['attach']
        for r in rewards:
            output_str = f'{T_CONST.ITEMS[int(r)]} {rewards[r]}'
            self.logger.info(output_str)
        reward_ships = json_obj['shipVO']
        for s in reward_ships:
            output_str = f'{s["title"]}'
            self.logger.info(output_str)

        self.set_adjutant_info(reward_res['adjutantData'])
        self.set_curr_points(reward_res['strategic_point'])
        sub_map = next((j for j in reward_res['shipVO'] if j['id'] == '10006'))['level_id']
        return sub_map
    """

    def reorder_battle_list(self, unorder: list) -> list:
        # Based on criteria mentioned in src/gui/tabs/thermopylae/constants.py
        res = []
        for cid in T_CONST.SUBMARINE_ORDER:
            i = 0
            while i < len(unorder):
                if self.user_ships[str(unorder[i])]['cid'] == cid:
                    res.append(unorder[i])
                    break
                else:
                    i += 1
            if len(res) == len(unorder):
                break
        return res

    def reset_ship_star(self) -> None:
        self.ship_star = {}

    def update_adjutant_info(self, adj_data: dict, strategic_point: int) -> None:
        # TODO: use signal? and manage signals globally?
        _name = T_CONST.ADJUTANT_ID_TO_NAME[adj_data['id']]
        _exp = f"Lv. {adj_data['level']} {adj_data['exp']}/{adj_data['exp_top']}"
        _point = str(strategic_point)

        self.adjutant_info = adj_data
        self.set_curr_points(strategic_point)
        self.tab_thermopylae.update_adjutant_name(_name)
        self.tab_thermopylae.update_adjutant_exp(_exp)
        self.logger.debug(self.get_adjutant_info())

# End of File
