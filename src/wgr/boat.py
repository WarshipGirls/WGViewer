from .api import WGR_API


class API_BOAT(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def supplyBoats(self, fleets: list):
        link = 'boat/supplyBoats/' + self._int_list_to_str(fleets) + '/0/0/'
        return self._api_call(link)

    def instantRepairShips(self, fleets: list):
        link = 'boat/instantRepairShips/' + self._int_list_to_str(fleets)
        return self._api_call(link)

    def changeEquipment(self, ship_id, equip_id, equip_slot):
        link = '/boat/changeEquipment/' + str(ship_id) + '/' + str(equip_id) + '/' + str(equip_slot)
        return self._api_call(link)

    def removeEquipment(self, ship_id, equip_slot):
        link = '/boat/removeEquipment/' + str(ship_id) + '/' + str(equip_slot)
        return self._api_call(link)


# End of File
