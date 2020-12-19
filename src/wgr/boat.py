from .api import WGR_API


class API_BOAT(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    # def changeBoat(self, fleet, ids, path)
    #     link = 'boat/changeBoat/' + fleet + '/' + ids + '/' + path + '/'
    #     return self._api_call(link)

    def changeEquipment(self, ship_id: str, equip_id: str, equip_slot: str):
        link = 'boat/changeEquipment/' + ship_id + '/' + equip_id + '/' + equip_slot
        return self._api_call(link)

    def instantFleet(self, fleet_id: str, ships: list):
        link = 'boat/instantFleet/' + fleet_id + '/' + self._int_list_to_str(ships) + '/'
        return self._api_urlopen(link)

    def instantRepairShips(self, ships: list):
        link = 'boat/instantRepairShips/' + self._int_list_to_str(ships) + '/'
        return self._api_urlopen(link)

    def lock(self, ship_id: str):
        # Assume this is a procedure before expedition
        link = 'boat/lock/' + ship_id + '/'
        return self._api_call(link)

    def removeBoat(self, fleet: str, ship_slot: str):
        link = 'boat/removeBoat/' + fleet + '/' + ship_slot + '/'
        return self._api_call(link)

    def removeEquipment(self, ship_id: str, equip_slot: str):
        link = 'boat/removeEquipment/' + ship_id + '/' + equip_slot
        return self._api_call(link)

    def renameShip(self, ship_id: str, new_name: str):
        link = 'boat/renameShip/' + ship_id + '/' + new_name + '/'
        # from urllib.request import quote
        # quote reference broken
        # link = quote(link, safe=";/?:@&=+$,", encoding="utf-8")
        return self._api_call(link)

    def repair(self, ship_id: str):
        link = 'boat/repair/' + ship_id + '/0/'
        return self._api_call(link)

    def repairComplete(self, dock_id: str, ship_id: str):
        link = 'boat/repairComplete/' + dock_id + '/' + ship_id + '/'
        return self._api_call(link)

    def rubdown(self, ship_id: str):
        # should use along with self.repair()
        link = 'boat/rubdown/' + ship_id
        return self._api_call(link)

    def strengthen(self, food: list, target_ship: str):
        link = 'boat/strengthen/' + self._int_list_to_str(food) + '/[' + target_ship + ']/'
        return self._api_urlopen(link)

    def skillLevelUp(self, ship_id: str):
        link = 'boat/skillLevelUp/' + ship_id + '/'
        return self._api_call(link)

    def supplyBoats(self, fleet: list):
        link = 'boat/supplyBoats/' + self._int_list_to_str(fleet) + '/0/0/'
        return self._api_urlopen(link)

# End of File
