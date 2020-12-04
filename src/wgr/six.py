from .api import WGR_API


class API_SIX(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def adjutantExp(self):
        # if success, exp + 5
        link = 'six/adjutantExp'
        return self._api_call(link)

    def canSelectList(self, is_refresh: str):
        # is_refresh = 0/1
        link = 'six/canSelectList/' + is_refresh
        return self._api_call(link)

    def challenge(self, formation: str):
        link = 'six/cha11enge/' + formation
        return self._api_call(link)

    def getUserData(self):
        link = 'six/getuserdata'        # no typo, all lowercase
        return self._api_call(link)

    def getFleetInfo(self):
        link = 'six/getFleetInfo'
        return self._api_call(link)

    def getPveData(self):
        link = 'six/getPveData'
        return self._api_call(link)

    def getWarResult(self, is_night: str = '0'):
        link = 'six/getWarResult/' + is_night
        return self._api_call(link)

    def newNext(self, node_id: str):
        link = 'six/newNext/' + node_id
        return self._api_call(link)

    def passLevel(self):
        link = 'six/passLevel'
        return self._api_call(link)

    def readyFire(self, sub_map_id: str):
        link = 'six/readyFire/' + sub_map_id
        return self._api_call(link)

    def selectBoat(self, selected_boats: list, skill_card: str = '0'):
        link = 'six/selectBoat/' + self._int_list_to_str(selected_boats) + '/' + skill_card
        return self._api_call(link)

    def setChapterBoat(self, sortie_map: str, fleets: list):
        # sortie_map from 9301 to 9318 in the order of E1 (9301,9302,9303) to E6 (9316,9317,9318)
        link = 'six/setChapterBoat/' + sortie_map + '/' + self._int_list_to_str(fleets)
        return self._api_call(link)

    def setWarFleet(self, fleets: list):
        link = 'six/setWarFleet/' + self._int_list_to_str(fleets)
        return self._api_call(link)

    def spy(self):
        link = 'six/spy'
        return self._api_call(link)

    def useAdjutant(self):
        # use adjutant skill
        link = 'six/useAdjutant'
        return self._api_call(link)

    def withdraw(self):
        link = 'six/withdraw'
        return self._api_call(link)


# End of File
