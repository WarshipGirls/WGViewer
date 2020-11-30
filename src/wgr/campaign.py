from .api import WGR_API


class API_CAMPAIGN(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def challenge(self, sortie_map: str, formation: str):
        link = 'campaign/challenge/' + sortie_map + '/' + formation + '/'
        return self._api_call(link)

    def getFleet(self, sortie_map: str):
        link = 'campaign/getFleet/' + sortie_map + '/'
        return self._api_call(link)

    def getUserData(self):
        link = 'campaign/getUserData'
        return self._api_call(link)

    def getWarResult(self, is_night: str = '0'):
        link = 'campaign/getWarResult/' + is_night + '/'
        return self._api_call(link)

    def spy(self, sortie_map: str):
        link = 'campaign/spy/' + sortie_map + '/'
        return self._api_call(link)

# End of File
