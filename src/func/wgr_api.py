import json

from .helper_function import Helper


class WGR_API:
    def __init__(self, server, channel, cookies):
        self.server = server
        self.channel = channel
        self.cookies = cookies
        self.hlp = Helper()

    def api_getShipList(self):
        url = self.server + 'api/getShipList' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        return data

    def api_initGame(self):
        url = self.server + 'api/initGame?&crazy=1' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        return data

    def boat_changeEquipment(self, ship_id, equip_id, equip_slot):
        url = self.server + '/boat/changeEquipment/' + str(ship_id) + '/' + str(equip_id) + '/' + str(equip_slot) + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        return data

    def boat_removeEquipment(self, ship_id, equip_slot):
        url = self.server + '/boat/removeEquipment/' + str(ship_id) + '/' + str(equip_slot) + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        return data

    def pve_getPveData(self):
        url = self.server + 'pve/getPveData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('pve_getPveData.json', 'w') as of:
            json.dump(data, of)

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


# End of File