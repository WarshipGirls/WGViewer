from .api import WGR_API


class API_FRIEND(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def getlist(self):
        link = 'friend/getlist/'
        return self._api_call(link)

    def kiss(self, uid: str):
        # to increase "love" value of a ship
        # max 1 call per ship, 5 calls total per day
        link = 'friend/kiss/' + uid
        return self._api_call(link)

    def visitorFriend(self, uid: str):
        link = 'friend/visitorFriend/' + uid + '/'
        return self._api_call(link)

# End of File
