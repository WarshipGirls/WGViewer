import json

from src.exceptions.wgr_error import get_error
from src.wgr.six import API_SIX


def save_json(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class PreSortieCheck:
    def __init__(self, api: API_SIX, is_realrun: bool):
        self.api: API_SIX = api
        self.is_realrun = is_realrun

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

# End of File
