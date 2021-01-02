"""
1. The implementation of auto E6 sortie is quite unnecessarily complicated at this point,
    please help improve the logic if possible! Many Thanks! - @pwyq
2. This is only meant for who passed E6 with 6SS; will not considering doing E1-E5 in the near future
    RIGHT NOW everything pre-battle is fixed
3. This file hosts high-level battle decisions; low-level pre/post processing code is host in ./helper.py
TODO: replace raise? this now creates a long series of frames
TODO free up dock space if needed
TODO: change all list to specific type, e.g. List[int]
"""

from typing import Union

from PyQt5.QtCore import QSettings

from src import data as wgv_data
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from src.func import qsettings_keys as QKEYS
from src.exceptions.wgr_error import get_error
from src.exceptions import custom as wgv_error
from src.utils import process_spy_json, set_sleep
from src.wgr import API_SIX
from .helper import SortieHelper
from .pre_sortie import PreSortieCheck
from . import constants as T_CONST

E61_0_ID: str = '931601'
E61_A1_ID: str = '931602'
E61_B1_ID: str = '931604'
E61_C1_ID: str = '931607'
E62_A1_ID: str = '931702'
E63_A1_ID: str = '931802'


class Sortie:
    # TODO: expedition thread will make this stop?
    def __init__(self, parent, api: API_SIX, dd: list, cv: list, main_fleet: list, is_realrun: bool):
        super().__init__()
        self.parent = parent
        self.api = api
        self.escort_DD = dd
        self.escort_CV = cv
        # TODO: bug, user selected SS are not set (old SS still used somehow)
        # self.main_fleet = main_fleet  # main fleet (6SS)
        self.main_fleet = [73239,75269,50773,16488,36848,132974]
        self.battle_fleet = set()  # ships that on battle
        self.logger = get_logger(QLOGS.TAB_THER)

        self.is_running: bool = True

        self.qsettings = QSettings(wgv_data.get_qsettings_file(), QSettings.IniFormat)
        if self.qsettings.contains(QKEYS.THER_REPAIRS):
            self.repair_levels: list = list(map(int, self.qsettings.value(QKEYS.THER_REPAIRS)))
        else:
            self.repair_levels: list = [2]

        # Used for pre-battle
        self.map_data: dict = {}
        self.user_data: dict = {}

        self.helper = None
        self.boat_pool: set = set()  # host existing boats
        self.curr_node: str = '0'
        self.curr_sub_map: str = '0'
        self.final_fleet: list = []  # fill up required number of boats
        self.tickets: int = 0
        self.user_ships: dict = wgv_data.get_processed_userShipVo()

        self.pre_sortie = PreSortieCheck(self.api, is_realrun)
        self.logger.info("Init E6...")

    def _clean_memory(self) -> None:
        self.logger.info("Reset ship card pool, battle fleet and curr node")
        self.helper.reset_ship_star()
        self.set_boat_pool([])
        self.set_fleet([])

    def _reset_chapter(self) -> None:
        # chapter can only be reset after E6-3
        if self.tickets <= 0:
            self.logger.warning("Insufficient sortie ticket. Cannot Reset Chapter")
            return
        reset_res = self.helper.reset_chapter(T_CONST.E6_ID)
        self._clean_memory()
        self.set_sub_map(T_CONST.SUB_MAP1_ID)
        self.helper.set_adjutant_info(reset_res['adjutantData'])
        self.update_sortie_ticket(ticket=reset_res['ticket'])

    def stop(self):
        self.is_running = False

    # ================================
    # Entry points
    # ================================

    def pre_battle(self) -> bool:
        self.logger.info("Start pre battle checking...")
        if self.pre_sortie.pre_battle_calls() is False:
            return False

        # Initialize necessary data
        self.map_data = self.pre_sortie.get_map_data()
        self.user_data = self.pre_sortie.get_user_data()
        self.curr_node = str(self.user_data['nodeId'])

        # Initialize SortieHelper
        self.helper = SortieHelper(self.parent, self.api, self.user_ships, self.map_data)
        self.helper.set_adjutant_info(self.user_data['adjutantData'])
        self.helper.set_curr_points(self.user_data['strategic_point'])

        ticket_num = int(self.user_data['canChargeNum']) - int(self.user_data['chargeNum'])
        self.parent.button_purchase.setEnabled(ticket_num > 0)
        self.update_sortie_ticket(ticket=self.user_data['ticket'], num=ticket_num)
        if self.qsettings.contains(QKEYS.THER_TKT_AUTO):
            if self.qsettings.value(QKEYS.THER_TKT_AUTO, type=bool) is True:
                self.buy_all_tickets(ticket_num)
            else:
                pass
        else:
            self.buy_all_tickets(ticket_num)
        self.update_adjutant_label(self.user_data['adjutantData'])
        self.set_boat_pool(self.user_data['boatPool'])
        self.set_sub_map(self.pre_sortie.get_sub_map_id())

        self.pre_battle_set_fleet()

        self.parent.button_stop_sortie.setEnabled(False)
        ticket_num = int(self.parent.ticket_label.text())
        if ticket_num > 0:
            self.parent.multi_runs.setMaximum(ticket_num)
            self.parent.multi_runs.setMinimum(0)
            self.parent.multi_runs.setValue(ticket_num)
            self.parent.multi_runs.setEnabled(True)
            self.parent.button_pre_battle.setEnabled(True)
            self.parent.button_fresh_sortie.setEnabled(True)
        else:
            self.parent.multi_runs.setValue(0)
            self.parent.multi_runs.setEnabled(False)
            self.parent.button_pre_battle.setEnabled(False)
            self.parent.button_fresh_sortie.setEnabled(False)
            self.logger.warning("Insufficient sortie ticket. Cannot start.")
            return False

        if len(self.boat_pool) > 0 and self.curr_node[-2:] != "01":
            self.parent.button_resume_sortie.setEnabled(True)
            self.logger.info('Can choose a fresh start or resume existing battle')
        else:
            self.logger.info('Can choose a fresh start')
        return True

    def pre_battle_set_fleet(self):
        # TODO: long long term: investigate the impact of selected ship costs on the random shop
        # this returned list length shall guarantee to meet the requirements
        prev_fleet = self.pre_sortie.get_final_fleet()
        user_selected = set(self.escort_DD + self.escort_CV + self.main_fleet)
        # Fill up the final fleet with arbitrary ships until the amount requirement is met
        if len(user_selected.difference(set(prev_fleet))) == 0:
            user_selected = prev_fleet
        else:
            while len(user_selected) < T_CONST.CHAP_FLEET_LEN[-1]:  # HARDCODING for now (only supports E6)
                x = prev_fleet.pop()
                ship = self.user_ships[str(x)]
                if ship['Class'] == 'SS':
                    continue
                user_selected.add(x)
        self.final_fleet = list(user_selected)

        self.logger.info("Setting final fleet:")
        for ship_id in self.final_fleet:
            ship = self.user_ships[str(ship_id)]
            output_str = "{:8s}{:17s}".format(str(ship_id), ship['Name'])
            if ship_id in self.main_fleet:
                output_str += "\tMAIN FORCE"
            elif ship_id in self.escort_DD:
                output_str += "\tESCORT DD"
            elif ship_id in self.escort_CV:
                output_str += "\tESCORT CV"
            else:
                pass
            # Lesson: do not output various stuff at once, concat them together; otherwise TypeError
            self.logger.info(output_str)

    def resume_sortie(self) -> bool:
        # TODO: may still have some corner cases to catch
        self.logger.info(f"[RESUME] Sortie {self.curr_node}")
        self.is_running = True

        try:
            self.helper.enter_sub_map(self.curr_sub_map)
            self.check_sub_map_done()

            if self.is_running is False:
                return False

            buy_res = None
            # Access shop for the first time
            shop_res = self.api.canSelectList('0')
            if 'eid' in shop_res:
                get_error(shop_res['eid'])
            elif '$ssss' in shop_res:
                self.logger.debug("[RESUME]: Visiting shop")
                ss_list = self.find_SS(shop_res['boats'])
                if (len(ss_list) == 0) and (shop_res['hadResetSelectFlag'] == 0):
                    # Access shop for the second time
                    shop_res = self.api.canSelectList('1')
                    ss_list = self.find_SS(shop_res['boats'])
                else:
                    pass
                is_buff = self.helper.is_buy_buff(self.curr_node)
                if len(ss_list) == 0:
                    pass
                else:
                    buy_res = self.buy_wanted_ships(purchase_list=ss_list, shop_data=shop_res, is_buff=is_buff)
            elif '$reset-$data' in shop_res and shop_res['$reset-$data'] is not None:
                self.logger.debug("[RESUME]: User has already used up purchase opportunity")
            else:
                self.logger.debug(shop_res)

            if buy_res is None:
                self.logger.debug("[RESUME] Use previous boat pool")
                self.set_fleet(self.user_data['boatPool'])
            else:
                self.logger.debug("[RESUME] Use new boat pool")
                self.set_boat_pool(boat_pool=buy_res['boatPool'])
                self.set_fleet(buy_res['boatPool'])

            if self.is_running is False:
                return False

            node_status = self.get_node_status(self.curr_node)
            self.logger.debug("node status = {}".format(node_status))
            if node_status == -1:
                self.logger.debug(self.curr_node)
                self.logger.debug(self.curr_sub_map)
                self.logger.debug(self.user_data['nodeList'])
            elif node_status == 3:
                next_node = self.helper.get_next_node_by_id(self.curr_node)
                while next_node not in T_CONST.BOSS_NODES:
                    if next_node == "-1":
                        raise wgv_error.ThermopylaeSortieExit("Quit on -1")
                    next_node = self.single_node_sortie(next_node)
                # boss fight
                self.single_node_sortie(next_node)
            elif node_status in [1, 2]:
                next_node = self.curr_node
                if node_status == 2:
                    next_node = self.resume_node_sortie(self.curr_node)
                while next_node not in T_CONST.BOSS_NODES:
                    if next_node == "-1":
                        raise wgv_error.ThermopylaeSortieExit("Quit on -1")
                    next_node = self.single_node_sortie(self.curr_node)
                # boss fight
                self.logger.info("[RESUME] Reaching Boss Node")
                self.single_node_sortie(next_node)
            else:
                self.logger.debug(self.curr_node)
        except wgv_error.ThermopylaeSortieExit as e:
            self.logger.warning(e)
            self.parent.button_fresh_sortie.setEnabled(True)
            return False
        except wgv_error.ThermopylaeSortieRestart as e:
            set_sleep()
            self.logger.warning(e)
            return self.start_fresh_sortie()
        except wgv_error.ThermopylaeSortieResume as e:
            set_sleep()
            self.logger.warning(e)
            return self.resume_sortie()
        except wgv_error.ThermopylaeSortieDone as e:
            self.logger.info(e)
            self._reset_chapter()
            return True

    def start_fresh_sortie(self) -> bool:
        self.is_running = True
        try:
            if self.curr_node == T_CONST.BOSS_NODES[2] and self.curr_sub_map == T_CONST.SUB_MAP3_ID:
                chapter_status = self.get_chapter_status(T_CONST.E6_ID)
                if chapter_status == 1:
                    self.curr_node = E61_0_ID
                    self.set_sub_map(T_CONST.SUB_MAP1_ID)
                elif chapter_status == 3:
                    self._reset_chapter()
                    pass
                else:
                    pass
            elif self.curr_node == "0" or self.curr_sub_map == "0" or self.curr_sub_map == T_CONST.SUB_MAP1_ID:
                self.curr_node = E61_0_ID
                self.set_sub_map(T_CONST.SUB_MAP1_ID)
                self._clean_memory()
                # TODO: test the following
                self.helper.set_chapter_fleet(T_CONST.E6_ID, self.final_fleet)
            else:
                pass
            next_id = self.starting_node()

            while next_id not in T_CONST.BOSS_NODES:
                if next_id == "-1":
                    raise wgv_error.ThermopylaeSortieExit("Quit on -1")
                next_id = self.single_node_sortie(next_id)
            self.logger.info("[FRESH] Reaching Boss Node")
            self.single_node_sortie(next_id)
        except wgv_error.ThermopylaeSortieExit as e:
            self.logger.warning(e)
            self.parent.button_fresh_sortie.setEnabled(True)
            return False
        except wgv_error.ThermopylaeSortieRestart as e:
            set_sleep()
            self.logger.warning(e)
            return self.start_fresh_sortie()
        except wgv_error.ThermopylaeSortieResume as e:
            set_sleep()
            self.logger.warning(e)
            return self.resume_sortie()
        except wgv_error.ThermopylaeSortieDone as e:
            self.logger.info(e)
            self._reset_chapter()
            return True

    # ================================
    # Getter / Setter (incl. UI)
    # ================================

    def get_chapter_status(self, chapter_id: str) -> int:
        try:
            node = next((i for i in self.user_data['chapterList'] if i['id'] == chapter_id))
            return int(node['status'])
        except StopIteration:
            return -1

    def get_node_status(self, node_id: str) -> int:
        try:
            node = next((i for i in self.user_data['nodeList'] if i['node_id'] == node_id))
            return node['status']
        except StopIteration:
            return -1

    def set_boat_pool(self, boat_pool: list) -> None:
        """
        Set the user's boat pool.
        @param boat_pool: current bought boats
        @type boat_pool: list of int
        @return: None
        @rtype: None
        """
        self.boat_pool = set(boat_pool)
        label_text = "BOAT POOL | "
        ship_star = self.helper.get_ship_star()
        for s in self.boat_pool:
            star_text = f"+{ship_star[str(s)]} " if str(s) in ship_star else ""
            label_text += f"{self.user_ships[s]['Name']} "
            label_text += star_text
        self.parent.update_boat_pool_label(label_text)

    def set_sub_map(self, sub_map_id: str) -> None:
        self.curr_sub_map = sub_map_id

    def update_adjutant_label(self, adj: dict) -> None:
        self.parent.update_adjutant_name(T_CONST.ADJUTANT_ID_TO_NAME[adj['id']])
        self.parent.update_adjutant_exp(f"Lv. {adj['level']} {adj['exp']}/{adj['exp_top']}")
        self.parent.update_points(str(self.user_data['strategic_point']))

    def update_battle_fleet_label(self, fleet: list) -> None:
        label_text = "ON BATTLE | "
        for s in fleet:
            label_text += f"{self.user_ships[str(s)]['Name']} "
        self.parent.update_fleet_label(label_text)

    def update_side_dock_repair(self, x) -> None:
        # assume only bucket is updated in packageVo; for more secure, use next()
        self.parent.update_repair_bucket(x[0]['num'])

    def update_side_dock_resources(self, x) -> None:
        self.parent.update_resources(x['oil'], x['ammo'], x['steel'], x['aluminium'])

    def update_side_dock_experience(self, x) -> None:
        self.parent.update_user_exp_label(x)

    def update_sortie_ticket(self, ticket: int = None, num: int = None) -> None:
        if ticket is None:
            self.parent.update_ticket(self.user_data['ticket'])
            self.tickets = int(self.user_data['ticket'])
        else:
            self.parent.update_ticket(str(ticket))
            self.tickets = ticket

        if num is None:
            self.parent.update_purchasable(self.user_data['canChargeNum'])
        else:
            self.parent.update_purchasable(str(num))

    # ================================
    # Helpers
    # ================================

    def buy_all_tickets(self, ticket_num):
        while ticket_num > 0:
            ticket_num = self.buy_ticket()
            set_sleep()

    def buy_ticket(self) -> int:
        if self.qsettings.contains(QKEYS.THER_TKT_RSC) is True:
            rsc = str(self.qsettings.value(QKEYS.THER_TKT_RSC))
        else:
            rsc = '3'
        buy_res = self.helper.charge_ticket(rsc)
        self.update_side_dock_resources(buy_res['userResVO'])
        # Weekly purchase quota is 3
        can_buy = 3 - buy_res['chargeNum']
        self.update_sortie_ticket(ticket=buy_res['ticket'], num=can_buy)
        self.parent.button_purchase.setEnabled(can_buy > 0)
        return can_buy

    def buy_wanted_ships(self, purchase_list: list, shop_data: dict, is_buff: bool) -> Union[None, dict]:
        """
        Given a list of ship ids, find all affordable ships

        @param purchase_list: a list of ship id(s)
        @type purchase_list: list of int
        @param shop_data: server response of six/canSelectList
        @type shop_data: dict
        @param is_buff: whether to buy buff at current node
        @type is_buff: bool
        @return:
            - None, if no ships can be bought
            - dict, server response of six/selectBoat
        @rtype: None, or a dict
        """
        purchase_list, buff_id = self.helper.find_affordable_ships(purchase_list=purchase_list, shop_data=shop_data, is_buff=is_buff)
        if len(purchase_list) == 0:
            buy_res = None
        else:
            buy_res = self.helper.buy_ships(purchase_list=purchase_list, shop_data=shop_data, buff_card=buff_id)
        return buy_res

    def check_sub_map_done(self) -> None:
        """
        Collects current sub map rewards if the sub map is done
        @return: Nothing
        @rtype: None
        """
        self.user_data = self.pre_sortie.fetch_user_data()
        curr_node = self.user_data['nodeId']
        self.helper.enter_sub_map(curr_node[:4])
        node_status = self.get_node_status(curr_node)

        self.logger.debug(curr_node)
        self.logger.debug(node_status)
        if (curr_node in T_CONST.BOSS_NODES) and (node_status == 3):
            self.helper.pass_sub_map()
            self.user_data = self.pre_sortie.fetch_user_data()
            self.set_sub_map(self.user_data['levelId'])
            if self.curr_sub_map == T_CONST.SUB_MAP3_ID and curr_node == T_CONST.BOSS_NODES[2]:
                raise wgv_error.ThermopylaeSortieDone("FINISHED ALL SUB MAPS!")
            else:
                raise wgv_error.ThermopylaeSortieRestart("Redo Final Boss Fight")
        else:
            pass

    def find_SS(self, shop_data: list) -> list:
        # Get from a list of int (max length of 5), return a list of ship_id (str)
        res = set()
        for ship_id in shop_data:
            if self.curr_node[:4] == T_CONST.SUB_MAP1_ID and ship_id in self.battle_fleet:
                # in E6-1, don't buy repeated ships
                continue
            if ship_id in self.main_fleet:
                res.add(str(ship_id))
        return list(res)

    def set_fleet(self, fleet: list) -> None:
        # The list may contain string or integer elements
        ss = []
        for s in fleet:
            if self.user_ships[s]['Class'] == "SS":
                ss.append(s)
        if len(ss) >= 4:
            temp = set([int(j) for j in ss])
            self.battle_fleet = set(self.helper.reorder_battle_list(list(temp)))
        else:
            self.battle_fleet = set(list(map(int, fleet)))

        if self.curr_node == E61_C1_ID:
            if len(ss) == 0:
                # endless-restarting loop; here appear inf times
                raise wgv_error.ThermopylaeSortieRestart("No SS for E61 C1. Restarting")
            else:
                self.battle_fleet = set(list(map(int, ss)))
        else:
            pass

        self.update_battle_fleet_label(list(self.battle_fleet))

    def starting_node(self) -> str:
        # First readyFire() let the server know the sub-map you are on
        self.helper.enter_sub_map(self.curr_sub_map)
        self.helper.retreat_sub_map()
        # Second readyFire
        next_node_id = self.helper.enter_sub_map(self.curr_sub_map)
        if self.is_running is False:
            return "-1"
        return self.single_node_sortie(next_node_id)

    # ================================
    # Combat
    # ================================

    def single_node_sortie(self, curr_node_id: str) -> str:
        self.curr_node = curr_node_id

        if self.is_running is False:
            return "-1"

        self.logger.info('********************************')
        self.logger.info("Start combat on {}".format(self.curr_node))
        self.logger.debug(self.helper.points)
        self.logger.debug(self.helper.adjutant_info)
        self.logger.info('********************************')

        self.helper.enter_next_node(str(curr_node_id))

        if curr_node_id == E61_A1_ID:
            shop_res = self.helper.get_ship_store()
            buy_res = self.helper.buy_ships(self.escort_DD, shop_res)
        elif curr_node_id == E61_B1_ID:
            shop_res = self.helper.get_ship_store()
            buy_res = self.helper.buy_ships(self.escort_CV, shop_res)
        else:
            # first shop fetch
            shop_res = self.helper.get_ship_store()
            ss_list = self.find_SS(shop_res['boats'])
            if len(ss_list) == 0:
                # second shop fetch
                set_sleep()
                shop_res = self.helper.get_ship_store('1')
                ss_list = self.find_SS(shop_res['boats'])
                if len(ss_list) == 0 and self.curr_node in [E61_C1_ID, E62_A1_ID, E63_A1_ID]:
                    raise wgv_error.ThermopylaeSortieRestart("SL to get SS on starting node of submaps")
                else:
                    pass
            else:
                pass
            is_buff = self.helper.is_buy_buff(self.curr_node)
            buy_res = self.buy_wanted_ships(purchase_list=ss_list, shop_data=shop_res, is_buff=is_buff)

        if self.is_running is False:
            return "-1"

        if buy_res is None:
            pass
        else:
            self.set_boat_pool(boat_pool=buy_res['boatPool'])
            self.set_fleet(buy_res['boatPool'])

        if self.is_running is False:
            return "-1"

        if curr_node_id in [E61_A1_ID, E62_A1_ID]:
            self.api.changeAdjutant(T_CONST.ADJUTANT_IDS[0])
            self.helper.cast_skill()
        elif curr_node_id == E63_A1_ID:
            self.api.changeAdjutant(T_CONST.ADJUTANT_IDS[2])  # Need to change everytime
            skill_res = self.helper.cast_skill()
            new_boat = skill_res['boat_add']
            if self.qsettings.contains(QKEYS.THER_HABA_REROLL):
                reroll_standard = self.qsettings.value(QKEYS.THER_HABA_REROLL, type=int)
            else:
                reroll_standard = 2
            if len(set(new_boat).intersection(set(self.main_fleet))) >= reroll_standard:
                self.boat_pool.union(new_boat)
            else:
                raise wgv_error.ThermopylaeSortieRestart("Bad luck with Habakkuk. Restarting")
        else:
            pass

        if curr_node_id == T_CONST.BOSS_NODES[0] and len(set(self.battle_fleet).intersection(set(self.main_fleet))) < 4:
            raise wgv_error.ThermopylaeSortieRestart("SS number less than 4 for E6-1 BOSS. Restarting")
        else:
            pass

        set_sleep()
        if self.is_running is False:
            return "-1"
        if set(self.battle_fleet) == set(self.final_fleet):
            self.logger.debug("Final fleet is set already. Skipping set")
        else:
            self.set_fleet(list(self.boat_pool))
            self.helper.set_war_fleet(list(self.battle_fleet))

        if self.helper.bump_level() == -1:
            raise wgv_error.ThermopylaeSortieRestart("Adjutant level bumping failed. Restarting")
        else:
            pass

        return self._complete_sortie(curr_node_id)

    def resume_node_sortie(self, curr_node_id: str) -> str:
        self.logger.info('********************************')
        self.logger.debug(self.helper.points)
        self.logger.debug(self.helper.adjutant_info)
        self.logger.info('********************************')
        self.helper.enter_sub_map(self.curr_node[:4])

        return self._complete_sortie(curr_node_id)

    def _complete_sortie(self, curr_node_id: str) -> str:
        set_sleep()
        if self.is_running is False:
            return "-1"
        supply_res = self.helper.supply_boats(list(self.battle_fleet))
        self.update_side_dock_resources(supply_res['userVo'])

        # pre-battle repair
        if (curr_node_id not in T_CONST.BOSS_NODES) and (curr_node_id not in T_CONST.REWARD_NODES):
            repair_res = self.helper.process_repair(supply_res['shipVO'], self.repair_levels)
        else:
            # repairs to full HP
            repair_res = self.helper.process_repair(supply_res['shipVO'], [1])
        if 'userVo' in repair_res:
            self.update_side_dock_resources(repair_res['userVo'])
            self.update_side_dock_repair(repair_res['packageVo'])

        set_sleep()
        if self.is_running is False:
            return "-1"
        spy_res = self.helper.scout_enemy()
        self.logger.info(process_spy_json(spy_res))

        set_sleep()
        if self.is_running is False:
            return "-1"
        formation = self.helper.get_challenge_formation(curr_node_id=self.curr_node, battle_fleet_size=len(self.battle_fleet))
        challenge_res = self.helper.challenge(formation)

        set_sleep(level=2)
        if self.is_running is False:
            return "-1"
        is_night_battle = self.helper.check_night_battle(curr_node_id, challenge_res)
        battle_res = self.helper.get_war_result(is_night_battle)
        self.update_side_dock_experience(battle_res['userLevelVo'])
        self.helper.process_battle_result(battle_res, list(self.battle_fleet))

        if int(battle_res['getScore$return']['flagKill']) == 1 or battle_res['resultLevel'] < 5:
            next_id = self.helper.get_next_node_by_id(battle_res['nodeInfo']['node_id'])
            if next_id != "" and next_id != "-1":
                self.logger.info(f"Next node: {self.helper.get_map_node_by_id(next_id)['flag']}")
            elif next_id == "":
                self.logger.info('---- BOSS NODE FINISHED ----')
            else:
                self.logger.error(f'Unexpected next node id: {next_id}')
        else:
            node_name = self.helper.get_map_node_by_id(self.curr_node)['flag']
            raise wgv_error.ThermopylaeSortieRestart(f"Failed to clean {node_name}. Restarting...")

        if self.is_running is False:
            return "-1"

        self.check_sub_map_done()
        return next_id

# End of File
