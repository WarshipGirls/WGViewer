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
SUBMARINE_ORDER = [
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
# TODO remove cross duplicate nodes
REWARD_NODES = ['931604', '931610', '931617', '931702', '931706', '931717', '931722', '931802', '931809', '931821']
BOSS_NODES = ['931617', '931722', '931821']
ADJUTANT_ID_TO_NAME = {'10082': "紫貂", '10182': "Kearsarge", '10282': "Habakkuk"}
ITEMS = {23: '战备券', 20041: '磁盘', 20141: '小型船舾装图纸', 20241: '中型船舾装图纸', 20341: '大型舰舾装图纸'}
SUBMAPID_TO_NAME = {'9316': "E6-1", '9317': "E6-2", '9318': "E6-3"}