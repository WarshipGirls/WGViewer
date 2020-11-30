import json
import logging

from requests import exceptions
from time import sleep

from .helper_function import Helper


class WGR_API:
    def __init__(self, server, channel, cookies):
        self.server = server
        self.channel = channel
        self.cookies = cookies

        self.hlp = Helper()
        self.max_retry = 10
        self.sleep_time = 5

    def _api_call(self, link):
        data = None
        url = self.server + link + self.hlp.get_url_end(self.channel)
        res = False
        tries = 0
        while not res:
            try:
                raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
                data = json.loads(raw_data)
                res = True
            except (TimeoutError, exceptions.ReadTimeout) as e:
                logging.error(e)
                logging.warning('Trying reconnecting...')
                sleep(self.sleep_time)
            tries += 1
            if tries >= self.max_retry:
                logging.warning(
                    f"Failed to connect to {link} after {self.max_retry} reconnections. Please try again later.")
                break
            else:
                pass
        return data

    @staticmethod
    def _int_list_to_str(int_list: list) -> str:
        return str(int_list).replace(' ', '')

    def api_getShipList(self):
        link = 'api/getShipList'
        return self._api_call(link)

    def api_initGame(self):
        link = 'api/initGame?&crazy=1'
        return self._api_call(link)

    def boat_changeEquipment(self, ship_id, equip_id, equip_slot):
        link = '/boat/changeEquipment/' + str(ship_id) + '/' + str(equip_id) + '/' + str(equip_slot)
        return self._api_call(link)

    def boat_removeEquipment(self, ship_id, equip_slot):
        link = '/boat/removeEquipment/' + str(ship_id) + '/' + str(equip_slot)
        return self._api_call(link)

    def pve_getPveData(self):
        url = self.server + 'pve/getPveData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('pve_getPveData.json', 'w') as of:
            json.dump(data, of)

    def six_getPveData(self):
        link = 'six/getPveData'
        return self._api_call(link)

    def six_getFleetInfo(self):
        link = 'six/getFleetInfo'
        return self._api_call(link)

    def six_getuserdata(self):
        link = 'six/getuserdata'
        return self._api_call(link)

    def six_setChapterBoat(self, sortie_map: int, fleets: list):
        # sortie_map from 9301 to 9318 in the order of E1 (9301,9302,9303) to E6 (9316,9317,9318)
        link = 'six/setChapterBoat/' + str(sortie_map) + '/' + self._int_list_to_str(fleets)
        return self._api_call(link)

    def six_readyFire(self, sub_map_id: int):
        link = 'six/readyFire/' + str(sub_map_id)
        return self._api_call(link)

    def six_newNext(self, node_id: int):
        link = 'six/newNext/' + str(node_id)
        return self._api_call(link)

    def six_canSelectList(self, is_refresh: int):
        # is_refresh = 0/1
        link = 'six/canSelectList/' + str(is_refresh)
        return self._api_call(link)

    def six_selectBoat(self, selected_boats: list, skill_card: int = 0):
        link = 'six/selectBoat/' + self._int_list_to_str(selected_boats)
        return self._api_call(link)

    def six_useAdjutant(self):
        # use adjutant skill
        link = 'six/useAdjutant'
        return self._api_call(link)

    def six_adjutantExp(self):
        # if success, exp + 5
        link = 'six/adjutantExp'
        return self._api_call(link)

    def six_setWarFleet(self, fleets: list):
        link = 'six/setWarFleet/' + self._int_list_to_str(fleets)
        return self._api_call(link)

    def boat_supplyBoats(self, fleets: list):
        link = 'boat/supplyBoats/' + self._int_list_to_str(fleets) + '/0/0/'
        return self._api_call(link)

    def boat_instantRepairShips(self, fleets: list):
        link = 'boat/instantRepairShips/' + self._int_list_to_str(fleets)
        return self._api_call(link)

    def six_spy(self):
        link = 'six/spy'
        return self._api_call(link)

    def six_cha11enge(self, formation: int):
        link = 'six/cha11enge/' + str(formation)
        return self._api_call(link)

    def six_getWarResult(self, is_night: int = 0):
        link = 'six/getWarResult/' + str(is_night)
        return self._api_call(link)

    def six_withdraw(self):
        link = 'six/withdraw'
        return self._api_call(link)

    def six_passLevel(self):
        link = 'six/passLevel'
        return self._api_call(link)

        # FOLLOWING ARE NOT USED YET

    '''

    def pevent_getPveData(self):
        url = self.server + 'pevent/getPveData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('pevent_getPveData.json', 'w') as of:
            json.dump(data, of)

    def bsea_getData(self):
        url = self.server + 'bsea/getData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('bsea_getData.json', 'w') as of:
            json.dump(data, of)

    def live_getUserInfo(self):
        url = self.server + 'live/getUserInfo' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('live_getUserInfo.json', 'w') as of:
            json.dump(data, of)

    # useless
    def six_getFleetInfo(self):
        url = self.server + 'six/getFleetInfo' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('six_getFleetInfo.json', 'w') as of:
            json.dump(data, of)

    def pve_getUserData(self):
        url = self.server + 'pve/getUserData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('pve_getUserData.json', 'w') as of:
            json.dump(data, of)

    def active_getUserData(self):
        url = self.server + 'active/getUserData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('active_getUserData.json', 'w') as of:
            json.dump(data, of)

    def task_getAchievementList(self):
        url = self.server + 'task/getAchievementList' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('task_getAchievementList.json', 'w') as of:
            json.dump(data, of)

    def campaign_getUserData(self):
        url = self.server + 'campaign/getUserData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('campaign_getUserData.json', 'w') as of:
            json.dump(data, of)
    '''

# End of File
