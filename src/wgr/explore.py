from .api import WGR_API


class API_EXPLORE(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def cancel(self, exp_map: str):
        link = 'explore/cancel/' + exp_map + '/'
        return self._api_call(link)

    def getResult(self, exp_map: str):
        link = 'explore/getResult/' + exp_map + '/'
        return self._api_call(link)

    def start(self, exp_map: str, fleet_id: str):
        link = 'explore/start/' + fleet_id + '/' + exp_map + '/'
        return self._api_call(link)

# End of File
