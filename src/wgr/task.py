from .api import WGR_API


class API_TASK(WGR_API):
    def __init__(self, cookies):
        super().__init__(cookies)

    def getAward(self, task_id: str):
        link = 'task/getAward/' + task_id + '/'
        return self._api_call(link)

    def getAchievementList(self, task_id: str):
        link = 'task/getAchievementList/' + task_id + '/'
        return self._api_call(link)

# End of File
