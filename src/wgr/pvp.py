from .api import WGR_API


class API_PVP(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def challenge(self, uid: str, fleet_id: str, formation: str):
        link = 'pvp/challenge/' + uid + '/' + fleet_id + '/' + formation + '/'
        return self._api_call(link)

    def getChallengeList(self):
        link = 'pvp/getChallengeList/'
        return self._api_call(link)

    def getWarResult(self, is_night: str):
        link = 'pvp/getWarResult/' + is_night + '/'
        return self._api_call(link)

    def spy(self, uid: str, fleet_id: str):
        link = 'pvp/spy/' + uid + '/' + fleet_id + '/'
        return self._api_call(link)

# End of File
