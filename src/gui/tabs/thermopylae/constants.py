# TODO: add these settings to GUI
# User Settings
BOSS_RETRY_LIMITS: list = [3, 5, 10]
CONNECTION_RETRY_LIMIT: int = 3
SHIP_REPAIR_LEVELS: list = [1]
# CONSTANTS
ADJUTANT_IDS: list = ['10082', '10181', '10282']
ADJUTANT_ID_TO_NAME: dict = {'10082': "紫貂", '10182': "Kearsarge", '10282': "Habakkuk"}
BOSS_NODES: list = ['931617', '931722', '931821']
ITEMS: dict = {23: '战备券', 20041: '磁盘', 20141: '小型船舾装图纸', 20241: '中型船舾装图纸', 20341: '大型舰舾装图纸'}
REWARD_NODES: list = ['931604', '931610', '931702', '931706', '931717', '931802', '931809']
SUBMAPID_TO_NAME: dict = {'9316': "E6-1", '9317': "E6-2", '9318': "E6-3"}
SUB_MAP1_ID: str = '9316'
SUB_MAP3_ID: str = '9318'
# Cost can be found in six/getPveData['combatBuff']; to save iteration time, copied only id-to-cost here
BUFF_BASE_COST: dict = {
    1001: 3, 1002: 2, 1003: 6, 1004: 6, 1005: 3,
    1006: 5, 1007: 4, 1008: 2, 1009: 5, 1010: 4
}
WORTH_BUYING_BUFFS: list = [
    1001,  # 肌肉记忆
    1002,  # 长跑训练
    1005,  # 黑科技
    1009,  # 关键一击
]
"""
The list is used to determine the order of submarines in E6 (thermopylae) battle fleet.
It is manually sorted, as of Game ver5.1.0, based on following criteria:
    - Mod I. > Non-Mod
    - With skill > without skill
    - High speed > low speed
    - German U-boats > rest         (only when U47-ModI.-SkillI. presents)
Since there are only 6 slots for a fleet, so top submarines matter only;
rest are for the sake of completeness.
"""
SUBMARINE_ORDER: list = [
    11035111,  # 'U-1405',
    11028911,  # 'U81',
    11019711,  # 'U47',
    11019511,  # 'Archerfish',
    11019411,  # 'Albacore',
    10036611,  # 'Nautilus',
    10029311,  # 'U1206',
    10035111,  # 'U-1405',
    10028911,  # 'U81'
    10019711,  # 'U47',
    10029211,  # 'U156',
    10019811,  # 'U505',
    10029011,  # 'U96',
    10045811,  # 'U-14',
    10040211,  # 'U-35',
    10038611,  # 'U-2365',
    10019511,  # '射水鱼',
    10019411,  # '大青花鱼',
    10029411,  # 'Tang',
    10040811,  # 'Barb',
    10036111,  # 'K1',
    10037311,  # '达·芬奇',
    10035911,  # '吕-34',
    10046311,  # '神鹰',
]
