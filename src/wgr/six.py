from .api import WGR_API
from .boat import API_BOAT


class API_SIX(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)
        self.boats_api = API_BOAT(cookies)

    # ================================
    # SIX
    # ================================

    def supplyBoats(self, fleet: list):
        return self.boats_api.supplyBoats(fleet)

    def instantRepairShips(self, fleet: list):
        return self.boats_api.instantRepairShips(fleet)

    # ================================
    # SIX
    # ================================

    def adjutantExp(self):
        # if success, exp + 5
        link = 'six/adjutantExp'
        return self._api_call(link)

    def canSelectList(self, is_refresh: str):
        # is_refresh = 0/1
        link = 'six/canSelectList/' + is_refresh
        return self._api_call(link)

    def changeAdjutant(self, adjutant_id: str):
        # 10082 / 10182 / 10282
        link = 'six/changeAdjutant/' + adjutant_id
        return self._api_call(link)

    def challenge(self, formation: str):
        link = 'six/cha11enge/' + formation
        return self._api_call(link)

    def chargeTicket(self, resource: str):
        # 0: fuel, 1: ammo, 2: steel, 3: bauxite
        link = 'six/chargeTicket/' + resource
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
        # !! NEED TO CALL THIS EVERYTIME YOU ENTER THE THERMOPYLAE MODE
        link = 'six/readyFire/' + sub_map_id
        return self._api_call(link)

    def resetChapter(self, sortie_map: str):
        # used when after passing the final sub-map of a chapter
        link = 'six/resetChapter/' + sortie_map
        return self._api_call(link)

    def selectBoat(self, selected_boats: list, skill_card: str = '0'):
        link = 'six/selectBoat/' + self._int_list_to_str(selected_boats) + '/' + skill_card
        return self._api_urlopen(link)

    def setChapterBoat(self, sortie_map: str, fleet: list):
        # chapter id: 10001 (E1) to 10006 (E6)
        link = 'six/setChapterBoat/' + sortie_map + '/' + self._int_list_to_str(fleet)
        return self._api_urlopen(link)

    def setWarFleet(self, fleet: list):
        link = 'six/setWarFleet/' + self._int_list_to_str(fleet)
        return self._api_urlopen(link)

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
