from .api import WGR_API


class API_DOCK(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def buildBoat(self, dock_id: str, fuel: str, ammo: str, steel: str, baux: str):
        link = 'dock/buildBoat/' + dock_id + '/' + fuel + '/' + ammo + '/' + steel + '/' + baux + '/'
        return self._api_call(link)

    def buildEquipment(self, dock_id: str, fuel: str, ammo: str, steel: str, baux: str):
        link = 'dock/buildEquipment/' + dock_id + '/' + fuel + '/' + ammo + '/' + steel + '/' + baux + '/'
        return self._api_call(link)

    def dismantleBoat(self, ships: list, save_equips: str = '1'):
        link = 'dock/dismantleBoat/[' + self._int_list_to_str(ships) + ']/' + save_equips + '/'
        return self._api_urlopen(link)

    def dismantleEquipment(self):
        # see #103 for TODO
        raise NotImplementedError
        # link = 'dock/dismantleEquipment/'
        # return self._api_call(link)

    def getBoat(self, dock_id: str):
        link = 'dock/getBoat/' + dock_id + '/'
        return self._api_call(link)

    def getEquipment(self, dock_id: str):
        link = 'dock/getEquipment/' + dock_id + '/'
        return self._api_call(link)

    def instantBuild(self, dock_id: str):
        link = 'dock/instantBuild/' + dock_id + '/'
        return self._api_call(link)

    def instantEquipmentBuild(self, dock_id: str):
        link = 'dock/instantEquipmentBuild/' + dock_id + '/'
        return self._api_call(link)

    def multBuildBoat(self, num: str, fuel: str, ammo: str, steel: str, baux: str):
        link = 'dock/multBuildBoat/' + num + '/' + fuel + '/' + ammo + '/' + steel + '/' + baux + '/'
        return self._api_call(link)

    def multBuildEquipment(self, num: str, fuel: str, ammo: str, steel: str, baux: str):
        link = 'dock/multBuildEquipment/' + num + '/' + fuel + '/' + ammo + '/' + steel + '/' + baux + '/'
        return self._api_call(link)

# End of File
