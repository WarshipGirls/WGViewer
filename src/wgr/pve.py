from .api import WGR_API


class API_PVE(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def challenge(self, sortie_map: str, fleet_id: str):
        link = 'pve/cha11enge/' + sortie_map + '/' + fleet_id + '/0/'
        return self._api_call(link)

    def dealto(self, node_id: str, fleet_id: str, formation: str):
        # start single node fight
        link = 'pve/dealto/' + node_id + '/' + fleet_id + '/' + formation + '/'
        return self._api_call(link)

    def getPveData(self):
        link = 'pve/getPveData'
        return self._api_call(link)

    def getUserData(self):
        link = 'pve/getUserData'
        return self._api_call(link)

    def getWarResult(self, is_night: str = '0'):
        link = 'pve/getWarResult/' + is_night
        return self._api_call(link)

    def newNext(self, node_id: str):
        link = 'pve/newNext/' + node_id
        return self._api_call(link)

    def spy(self):
        link = 'pve/spy'
        return self._api_call(link)

    def skipWar(self):
        link = 'pve/SkipWar'
        return self._api_call(link)

# End of File
