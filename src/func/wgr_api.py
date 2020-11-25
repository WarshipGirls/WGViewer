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


# End of File