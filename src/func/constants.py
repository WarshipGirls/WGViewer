
version = "5.0.0"

pvp_attempt_limit = 20

header = {
    'Accept-Encoding': 'identity',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9.1.1; SAMSUNG-SM-G900A Build/LMY47X)'
}

android_data_dict = {
    'client_version': version,
    'phone_type': 'samsung note 9',
    'phone_version': '9.1.1',
    'ratio': '2960*1440',
    'service': 'CHINA MOBILE',
    'udid': '',
    'source': 'android',
    'affiliate': 'WIFI',
    't': '-1',
    'e': '-1',
    'gz': '1',
    'market': '2',
    'channel': '100015',
    'version': version
}

ios_data_dict = {
    'client_version': version,
    'phone_type': '',
    'phone_version': '13.7',
    'ratio': '2160*1620',
    'service': '',
    'udid': '',
    'source': 'ios',
    'affiliate': 'WIFI',
    't': '-1',
    'e': '-1',
    'gz': '1',
    'market': '2',
    'channel': '100020',
    'version': version
}

login_key = "kHPmWZ4zQBYP24ubmJ5wA4oz0d8EgIFe"

repair_types = {
    0: "Minor Damage Repair",
    1: "Moderate Damage Repair",
    2: "Heavy Damage Rapair"
}

# expedition; unit = seconds
exp_durations = {
    "10001": 900,
    "10002": 1800,
    "10003": 1800,
    "10004": 3600,
    "20001": 7200,
    "20002": 2700,
    "30001": 14400,
    "40001": 14400,
    "60001": 32400
}

eid_codes = {
    "-1206": "fails getting login reward...",
    "-604": "fails starting explore...",
    "-602": "fails getting current running explore...",
    "-601": "fails getting empty explore...",
    "-906": "no warReport...err occur when try to do 2nd pvp",
    "-905": "no warReport...err occur when try to do friend pvp",
    "-103": "no warReport...Maybe map/opponent is not accessible OR sortie too fast",
    "-401": "fail to access unavailable map",
    "-408": "NO SUPPLY!!",
    "-215": "FULL DOCK!!",
    "-209": "cannot find war report...",
    "-1": "FAIL to instant repair!!",
    "-9993":"link not exist??",
    "-2505": "shop re-roll failed",
    "-1608": "ship kiss failed",
    "-127": "Logging failed"
}

war_eval = ['-', 'SS', 'S', 'A', 'B', 'C', 'D']

reward_type = {
    2: '油', 3: '弹', 4: '钢', 9: '铝', 10141: "CV-core", 10241: 'BB-core', 10341: 'CA-core', 10441: 'DD-core',
    10541: 'SS-core', 141: 'inst-build', 241: 'build-blueprint', 541: 'inst-repair', 741: 'equip-blueprint', 66641: 'dmg-ctrl',
    11042: '港区周年藏品'
}


ship_type = {
    1: "CV",
    2: "CVL",
    3: "AV",
    4: "BB",
    5: "BBV",
    6: "BC",
    7: "CA",
    8: "CAV",
    9: "CLT",
    10: "CL",
    11: "BM",
    12: "DD",
    13: "SSV",
    14: "SS",
    15: "SC",
    16: "AP",
    17: "ASDG",
    18: "AADG"
}

build_type = {
    1: "Type S.",
    2: "Type M.",
    3: "Type L.",
    4: "?",
    5: "?"
}

air_control = {
    1: "Air Supremacy",
    2: "Air Superiority",
    3: "Air Parity",
    4: "Air Denial",
    5: "Air Incapability"
}

formation = {
    1: "单纵 LineAhead",
    2: "复纵 DoubleLine",
    3: "轮形 Diamond",
    4: "T形 Echelon",
    5: "单横 LineAbreast"
}
