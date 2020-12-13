import json

from logging import getLogger

from src.exceptions.wgr_error import get_error
from src.utils.general import set_sleep
from src.wgr.six import API_SIX
from . import constants as T_CONST


def save_json(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class PreSortieCheck:
    def __init__(self, api: API_SIX, is_realrun: bool):
        self.api: API_SIX = api
        self.is_realrun = is_realrun

        self.logger = getLogger('TabThermopylae')
        self.final_fleet: list = []
        self.sub_map_id: str = ""
        self.map_data: dict = {}
        self.user_data: dict = {}

    # ================================
    # Fetch Server Response
    # ================================

    def fetch_fleet_info(self) -> dict:
        fleet_info: dict = self.api.getFleetInfo()
        if 'eid' in fleet_info:
            get_error(fleet_info['eid'])
            return {}
        if self.is_realrun is False:
            save_json('six_getFleetInfo.json', fleet_info)
        return fleet_info

    def fetch_map_data(self) -> dict:
        map_data: dict = self.api.getPveData()
        if 'eid' in map_data:
            get_error(map_data['eid'])
            return {}
        if self.is_realrun is False:
            save_json('six_getPveData.json', map_data)
        return map_data

    def fetch_user_data(self) -> dict:
        user_data: dict = self.api.getUserData()
        if 'eid' in user_data:
            get_error(user_data['eid'])
            return {}
        if self.is_realrun is False:
            save_json('six_getUserData.json', user_data)
        return user_data

    # ================================
    # Pre Battle Checkings
    # ================================

    def pre_battle_validation(self, user_data: dict) -> bool:
        # Insepect the validity for user to use this function
        user_e6 = next(i for i in user_data['chapterList'] if i['id'] == "10006")
        if user_data['chapterId'] != '10006':
            self.logger.warning("You are in the middle of a battle other than E6. Exiting")
            return False
        elif len(user_e6['boats']) != 22:
            self.logger.warning("You have not passed E6 manually. Exiting")
            return False
        else:
            pass

        # check if the sortie "final fleet" is set or not
        fleet_info = self.fetch_fleet_info()
        b = fleet_info['chapterInfo']['boats']
        if len(b) == 0:
            self.logger.info('User has not entered E6. Select from old settings')
            self.sub_map_id = fleet_info['chapterInfo']['level_id']
            last_fleets = user_e6['boats']
        elif len(b) == 22 and fleet_info['chapterInfo']['level_id'] in T_CONST.SUB_MAP_IDS:
            self.logger.info('User has entered E6.')
            self.sub_map_id = fleet_info['chapterInfo']['level_id']
            last_fleets = b
        else:
            self.logger.info('Invalid settings for using this function')
            self.logger.info('1. Ensure you have cleared E6-3; 2. You are not in a battle OR in E6')
            return False

        if len(last_fleets) != 22:
            self.logger.warning("Invalid last boats settings.")
            res = False
        else:
            self.final_fleet = last_fleets
            res = True
        return res

    def pre_battle_calls(self) -> bool:
        self.map_data = self.fetch_map_data()
        set_sleep()
        self.user_data = self.fetch_user_data()
        set_sleep()

        if self.pre_battle_validation(self.user_data) is False:
            self.logger.warning("Failed to pre-battle checking due to above reason.")
            return False
        else:
            self.logger.info("Pre-battle checking is done.")
            return True

    # ================================
    # Getter
    # ================================

    def get_final_fleet(self) -> list:
        return self.final_fleet

    def get_map_data(self) -> dict:
        return self.map_data

    def get_sub_map_id(self) -> str:
        return self.sub_map_id

    def get_user_data(self) -> dict:
        return self.user_data

# End of File
