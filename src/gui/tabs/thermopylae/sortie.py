"""
The implementation of auto E6 sortie is quite unnecessarily complicated at this point,
please help improve the logic if possible! Many Thanks! - @pwyq


This is only meant for who passed E6 with 6SS; will not considering doing E1-E5 in the near future
RIGHT NOW everything pre-battle is fixed
TODO: multiple consecutive run w/o interference
TODO: replace raise?
TODO free up dock space if needed
TODO: remove all hard coding
TODO: refactor

WGR BUG:
- if you withdraw and re-enter a sub map w/o readyFire, then your adjutant data is not reset
    - i.e. you can quit E6-1Boss and restart w/o calling readyFire, you can have Lv.5 adjutant at the beginning
"""

from logging import getLogger

from src import data as wgv_data
from src.exceptions.wgr_error import get_error
from src.exceptions.custom import ThermopylaeSoriteExit, ThermopylaeSortieRestart, ThermopylaeSortieResume, ThermopylaeSortieDone
from src.utils.general import set_sleep
from src.wgr.six import API_SIX
from .helper import SortieHelper
from .pre_sortie import PreSortieCheck
from . import constants as T_CONST


class Sortie:

    def __init__(self, parent, api: API_SIX, fleet: list, final_fleet: list, is_realrun: bool):
        super().__init__()
        self.parent = parent
        self.api: API_SIX = api
        self.main_fleet = fleet  # main fleets (6SS)
        self.battle_fleet = set()  # ships that on battle
        self.final_fleet = final_fleet  # fill up required number of boats
        self.logger = getLogger('TabThermopylae')

        # Used for pre-battle
        self.map_data = None
        self.user_data = None

        self.helper = None
        self.curr_node: str = '0'
        self.curr_sub_map: str = '0'
        self.boat_pool: set = set()  # host existing boats
        self.escort_DD = []  # For 2DD to pass first few levels only, 萤火虫，布雷恩
        self.escort_CV = []  # For 1CV to pass first few levels only, 不挠
        self.user_ships = wgv_data.get_processed_userShipVo()

        self.pre_sortie = PreSortieCheck(self.api, is_realrun)
        self.logger.info("Init E6...")

    def _clean_memory(self) -> None:
        self.logger.info("Reset ship card pool, battle fleet and curr node")
        self.set_boat_pool([])
        self.set_fleet([])

    # ================================
    # Pre battle checke
    # ================================

    def pre_battle_set_info(self) -> bool:
        # Insepect the validity for user to use this function
        user_e6 = next(i for i in self.user_data['chapterList'] if i['id'] == "10006")
        if self.user_data['chapterId'] != '10006':
            self.logger.warning("You are in the middle of a battle other than E6. Exiting")
            return False
        elif len(user_e6['boats']) != 22:
            self.logger.warning("You have not passed E6 manually. Exiting")
            return False
        else:
            pass
        self.set_sortie_tickets()
        self.update_adjutant_label()

        # check if the sortie "final fleet" is set or not
        fleet_info = self.pre_sortie.fetch_fleet_info()
        b = fleet_info['chapterInfo']['boats']
        if len(b) == 0:
            self.logger.info('User has not entered E6. Select from old settings')
            last_fleets = user_e6['boats']
        elif len(b) == 22 and fleet_info['chapterInfo']['level_id'] in ['9316', '9317', '9318']:
            self.logger.info('User has entered E6.')
            self.set_sub_map(fleet_info['chapterInfo']['level_id'])
            last_fleets = b
        else:
            self.logger.info('Invalid settings for using this function')
            self.logger.info('1. Ensure you have cleared E6-3; 2. You are not in a battle OR in E6')
            return False

        self.set_boat_pool(self.user_data['boatPool'])
        self.curr_node = str(self.user_data['nodeId'])

        if len(last_fleets) != 22:
            self.logger.warning("Invalid last boats settings.")
            res = False
        else:
            self.final_fleet = last_fleets
            res = True
        return res

    def pre_battle_calls(self) -> bool:
        self.map_data = self.pre_sortie.fetch_map_data()
        set_sleep()
        self.user_data = self.pre_sortie.fetch_user_data()
        set_sleep()

        if self.pre_battle_set_info() is False:
            self.logger.warning("Failed to pre-battle checking due to above reason.")
            return False
        else:
            self.logger.warning("Pre-battle checking is done.")
            return True

    def pre_battle(self) -> None:
        self.logger.info("Start pre battle checking...")

        if self.pre_battle_calls() is False:
            return

        # init data
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
        if len(self.boat_pool) > 0 and self.curr_node[-2:] != "01":
            self.parent.button_resume_sortie.setEnabled(True)
            self.logger.info('Can choose a fresh start or resume existing battle')
        else:
            self.logger.info('Can choose a fresh start')

    # ================================
    # Entry points
    # ================================

    def check_sub_map_done(self, curr_node: str) -> None:
        self.pre_sortie.fetch_user_data()
        curr_node = self.user_data['nodeId']

        self.helper.api_readyFire(curr_node[:4])
        node_status = self.get_node_status(curr_node)
        print("//////////////////////////////")
        print(curr_node)
        print(node_status)
        print("//////////////////////////////")
        if (curr_node in T_CONST.BOSS_NODES) and (node_status == 3):
            self.helper.api_passLevel()
            self.pre_sortie.fetch_user_data()
            self.set_sub_map(self.user_data['levelId'])
            if self.curr_sub_map == '9318' and curr_node == '931821':
                raise ThermopylaeSortieDone("FINISHED ALL SUB MAPS!")
            else:
                raise ThermopylaeSortieRestart("BOSS FIGHT DONE!")

    def _reset_chapter(self) -> None:
        # chapter can only be reset after E6-3
        reset_res = self.helper.reset_chapter('10006')
        self.set_boat_pool([])
        self.set_fleet([])
        self.set_sub_map('9316')
        self.helper.set_adjutant_info(reset_res['adjutantData'])
        self.set_sortie_tickets(ticket=reset_res['ticket'])

    def resume_sortie(self) -> None:
        # TODO: still have some corner cases to catch
        self.logger.info(f"Resume sortie from node {self.curr_node}")
        try:
            self.helper.api_readyFire(self.curr_sub_map)
            self.check_sub_map_done(self.curr_node)

            shop_res = self.api.canSelectList('0')
            # TODO simplify this giant if-else
            if 'eid' in shop_res:
                get_error(shop_res['eid'])
                buy_res = None
            elif '$ssss' in shop_res:
                self.logger.debug('trying visiting store')
                if shop_res['hadResetSelectFlag'] == 0:
                    ss_list = self.find_SS(shop_res['boats'])
                    if len(ss_list) == 0:
                        # do a second fetch
                        shop_res = self.api.canSelectList('1')
                        ss_list = self.find_SS(shop_res['boats'])
                        if len(ss_list) == 0:
                            buy_res = None
                        else:
                            purchase_list = self.helper.find_affordable_ships(ss_list, shop_res)
                            if len(purchase_list) > 0:
                                buy_res = self.helper.buy_ships(purchase_list, shop_res)
                            else:
                                buy_res = None
                    else:
                        purchase_list = self.helper.find_affordable_ships(ss_list, shop_res)
                        if len(purchase_list) > 0:
                            buy_res = self.helper.buy_ships(purchase_list, shop_res)
                        else:
                            buy_res = None
                else:
                    ss_list = self.find_SS(shop_res['boats'])
                    if len(ss_list) == 0:
                        buy_res = None
                    else:
                        purchase_list = self.helper.find_affordable_ships(ss_list, shop_res)
                        if len(purchase_list) > 0:
                            buy_res = self.helper.buy_ships(purchase_list, shop_res)
                        else:
                            buy_res = None
            elif '$reset-$data' in shop_res and shop_res['$reset-$data'] is not None:
                self.logger.debug('user has already used up purchase opportunity')
                buy_res = None
            else:
                self.logger.debug(shop_res)
                buy_res = None

            if buy_res is None:
                self.logger.debug("using previous boat pool")
                self.set_fleet(self.user_data['boatPool'])
            else:
                self.logger.debug("using new boat pool")
                self.set_boat_pool(buy_res['boatPool'])
                self.set_fleet(buy_res['boatPool'])

            node_status = self.get_node_status(self.curr_node)
            print("node status = {}".format(node_status))
            if node_status == -1:
                print(self.curr_node)
                print(self.curr_sub_map)
                print(self.user_data['nodeList'])
                self.logger.error('Unexpected node. Should do a fresh start.')
            elif node_status == 3:
                next_node = self.helper.get_next_node_by_id(self.curr_node)
                while next_node not in T_CONST.BOSS_NODES:
                    next_node = self.single_node_sortie(next_node)
                # boss fight
                self.single_node_sortie(next_node)
            elif node_status in [1, 2]:
                next_node = self.curr_node
                if node_status == 2:
                    next_node = self.resume_node_sortie(self.curr_node)
                while next_node not in T_CONST.BOSS_NODES:
                    next_node = self.single_node_sortie(self.curr_node)
                # boss fight
                self.logger.info("!! REACHING BOSS NODE 2 !!")
                self.single_node_sortie(next_node)
            else:
                self.logger.debug(self.curr_node)
        except ThermopylaeSoriteExit as e:
            self.logger.debug(e)
            self.parent.button_fresh_sortie.setEnabled(True)
            return
        except ThermopylaeSortieRestart as e:
            set_sleep()
            self.logger.debug(e)
            self.start_fresh_sortie()
        except ThermopylaeSortieResume as e:
            set_sleep()
            self.logger.debug(e)
            self.resume_sortie()
        except ThermopylaeSortieDone as e:
            self.logger.info(e)
            self._reset_chapter()

    def start_fresh_sortie(self) -> None:
        try:
            if self.curr_node == "0" or self.curr_sub_map == "0":
                self._clean_memory()
                self.api.setChapterBoat('10006', self.final_fleet)
                self.curr_node = '931601'
                self.curr_sub_map = '9316'
            next_id = self.starting_node()

            while next_id not in T_CONST.BOSS_NODES:
                next_id = self.single_node_sortie(next_id)
            self.logger.info("!! REACHING BOSS NODE 1 !!")
            self.single_node_sortie(next_id)
        except ThermopylaeSoriteExit as e:
            self.logger.debug(e)
            self.parent.button_fresh_sortie.setEnabled(True)
            return
        except ThermopylaeSortieRestart as e:
            set_sleep()
            self.logger.debug(e)
            self.start_fresh_sortie()
        except ThermopylaeSortieResume as e:
            set_sleep()
            self.logger.debug(e)
            self.resume_sortie()
        except ThermopylaeSortieDone as e:
            self.logger.info(e)
            self._reset_chapter()

    # ================================
    # Setter / Getter
    # ================================

    def get_node_status(self, node_id: str) -> int:
        try:
            node = next((i for i in self.user_data['nodeList'] if i['node_id'] == node_id))
            return node['status']
        except StopIteration:
            return -1

    def set_sub_map(self, sub_map_id: str) -> None:
        self.curr_sub_map = sub_map_id

    def set_sortie_tickets(self, ticket: int = None, num: int = None) -> None:
        if ticket is None:
            self.parent.update_ticket(self.user_data['ticket'])
        else:
            self.parent.update_ticket(str(ticket))

        if num is None:
            self.parent.update_purchasable(self.user_data['canChargeNum'])
        else:
            self.parent.update_purchasable(str(num))

    def update_adjutant_label(self) -> None:
        adj = self.user_data['adjutantData']
        self.parent.update_adjutant_name(T_CONST.ADJUTANT_ID_TO_NAME[adj['id']])
        self.parent.update_adjutant_exp(f"Lv. {adj['level']} {adj['exp']}/{adj['exp_top']}")
        self.parent.update_points(str(self.user_data['strategic_point']))

    def set_boat_pool(self, boat_pool: list) -> None:
        self.boat_pool = set(boat_pool)
        label_text = "BOAT POOL | "
        for s in self.boat_pool:
            label_text += f"{self.user_ships[s]['Name']} "
        self.parent.update_boat_pool_label(label_text)

    def set_fleet(self, fleet: list) -> None:
        # The list may contain string or integer elements
        ss = []
        for s in fleet:
            if self.user_ships[s]['Class'] == "SS":
                ss.append(s)
        if len(ss) >= 4:
            temp = set([int(j) for j in ss])
            self.battle_fleet = self.helper.reorder_battle_list(list(temp))
        else:
            self.battle_fleet = set([int(j) for j in fleet])

        if self.curr_node == '931607':
            if len(ss) == 0:
                # TODO: this is not covered; a raise is before this one
                raise ThermopylaeSoriteExit
            else:
                self.battle_fleet = set([int(j) for j in ss])
        else:
            pass

        self.update_battle_fleet_label(list(self.battle_fleet))

    def update_battle_fleet_label(self, fleet: list) -> None:
        label_text = "ON BATTLE | "
        for s in fleet:
            label_text += f"{self.user_ships[str(s)]['Name']} "
        self.parent.update_fleet_label(label_text)

    def update_side_dock_resources(self, x) -> None:
        self.parent.update_resources(x['oil'], x['ammo'], x['steel'], x['aluminium'])

    def update_side_dock_repair(self, x) -> None:
        # assume only bucket is updated in packageVo; for more secure, use next()
        self.parent.update_repair_bucket(x[0]['num'])

    # ================================
    # Combat
    # ================================

    def starting_node(self) -> str:
        # First let the server know which sub-map you are on; otherwise without this, withdraw resets to the first sub-map
        print(self.curr_node)
        print(self.curr_sub_map)
        self.helper.api_readyFire(self.curr_sub_map)
        self.helper.api_withdraw()
        # second readyFire
        next_node_id = self.helper.api_readyFire(self.curr_sub_map)
        return self.single_node_sortie(next_node_id)

    def find_SS(self, shop_data: list) -> list:
        # Get from a list of int (max length of 5), return a list of ship_id (str)
        res = set()
        for ship_id in shop_data:
            if self.curr_node[:4] == '9316' and ship_id in self.battle_fleet:
                # in E6-1, don't buy repeated ships
                continue
            if ship_id in self.main_fleet:
                res.add(str(ship_id))
        return list(res)

    def single_node_sortie(self, curr_node_id: str) -> str:
        self.curr_node = curr_node_id
        self.logger.info('********************************')
        self.logger.info("Start combat on {}".format(self.curr_node))
        self.logger.info(self.helper.points)
        self.logger.info(self.helper.adjutant_info)
        self.logger.info('********************************')
        self.helper.api_newNext(str(curr_node_id))

        buy_res = None
        if curr_node_id == '931602':
            shop_res = self.helper.get_ship_store()
            buy_res = self.helper.buy_ships(self.escort_DD, shop_res)
        elif curr_node_id == '931604':
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
                if len(ss_list) == 0 and self.curr_node in ['931607', '931702', '931802']:
                    raise ThermopylaeSortieRestart
                else:
                    pass
            else:
                pass

            purchase_list = self.helper.find_affordable_ships(ss_list, shop_res)
            if len(purchase_list) > 0:
                buy_res = self.helper.buy_ships(purchase_list, shop_res)

        if buy_res is None:
            pass
        else:
            self.set_boat_pool(buy_res['boatPool'])
            self.set_fleet(buy_res['boatPool'])

        if curr_node_id in ['931602', '931702']:
            self.api.changeAdjutant('10082')
            # TODO: check adjutnat level
            self.helper.cast_skill()
        elif curr_node_id == '931802':
            # TODO: move to helper; and put before 9318
            self.api.changeAdjutant('10282')
            skill_res = self.helper.cast_skill()
            new_boat = skill_res['boat_add']
            if len(set(new_boat).intersection(set(self.main_fleet))) >= 2:
                self.boat_pool.union(new_boat)
            else:
                raise ThermopylaeSortieRestart("Bad luck with Habakkuk; Restart")
        else:
            pass

        set_sleep()
        if set(self.battle_fleet) == set(self.final_fleet):
            self.logger.debug('final fleet is done. skip setting!')
        else:
            self.set_fleet(list(self.boat_pool))
            self.helper.set_war_fleets(list(self.battle_fleet))

        if self.helper.check_adjutant_level_bump() == 0:
            if self.helper.bump_level() is False:
                self.logger.info('Bumping failed. Should restart current sub-map.')
            else:
                pass
        else:
            pass

        return self.one_sortie(curr_node_id)

    def resume_node_sortie(self, curr_node_id: str) -> str:
        self.logger.info('********************************')
        self.logger.info("Resume combat on {}".format(curr_node_id))
        self.logger.info(self.helper.points)
        self.logger.info(self.helper.adjutant_info)
        self.logger.info('********************************')
        self.helper.api_readyFire(self.curr_node[:4])

        return self.one_sortie(curr_node_id)

    def one_sortie(self, curr_node_id: str) -> str:
        # TODO: get a more informative name

        set_sleep()
        supply_res = self.helper.supply_boats(list(self.battle_fleet))
        self.update_side_dock_resources(supply_res['userVo'])

        repair_res = self.helper.process_repair(supply_res['shipVO'], T_CONST.SHIP_REPAIR_LEVELS)  # pre-battle repair
        if 'userVo' in repair_res:
            self.update_side_dock_resources(repair_res['userVo'])
            self.update_side_dock_repair(repair_res['packageVo'])

        set_sleep()
        self.helper.spy()

        set_sleep()
        formation = self.helper.get_challenge_formation(curr_node_id=self.curr_node, battle_fleet_size=len(self.battle_fleet))
        challenge_res = self.helper.challenge(formation)

        set_sleep(level=2)
        is_night_battle = self.helper.check_night_battle(curr_node_id, challenge_res)
        battle_res = self.helper.get_war_result(is_night_battle)
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
            self.logger.info(f"Failed to clean {self.helper.get_map_node_by_id(self.curr_node)['flag']}. Restarting...")
            raise ThermopylaeSortieRestart

        self.check_sub_map_done(next_id)
        return next_id

# End of File
