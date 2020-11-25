#	Result	Protocol	Host	URL	Body	Caching	Content-Type	Process	Comments	Custom	
# /boat/removeEquipment/169794/0&t=1606277123774&e=41bf6051fa3a4f0fb3af8db3aa9b2a11&version=4.10.0&channel=100011&gz=1&market=3			
# /boat/changeEquipment/169792/10007921/0&t=1606277134797&e=fe81104cc94942b99c6fad34c1bb0274&version=4.10.0&channel=100011&gz=1&market=3			
# To find API, use Fiddler.
import json

from .helper_function import Helper


class WGR_API:
    def __init__(self, server, channel, cookies):
        self.server = server
        self.channel = channel
        self.cookies = cookies
        self.hlp = Helper()

    def boat_changeEquipment(self, ship_id, equip_id, equip_slot):
        url = self.server + '/boat/changeEquipment/' + str(ship_id) + '/' + str(equip_id) + '/' + str(equip_slot) + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        return data

    def boat_removeEquipment(self, ship_id, equip_slot):
        url = self.server + '/boat/removeEquipment/' + str(ship_id) + '/' + str(equip_slot) + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        print(data)


# End of File