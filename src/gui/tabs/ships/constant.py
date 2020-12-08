# Whenever changed following options, double check proxy model
lock_select = ["ALL", "YES", "NO"]
level_select = ["ALL", "Lv. 1", "> Lv. 1", "\u2265 Lv. 90", "\u2265 Lv. 100", "= Lv. 110"]
value_select = ["Curr. (w/ Equip.)", "Max. (w/ Equip.)", "Raw (w/o Equip.)"]
mod_select = ["ALL", "Non-mod.", "Mod. I"]
rarity_select = ["ALL", "\u2606 1", "\u2606 2", "\u2606 3", "\u2606 4", "\u2606 5", "\u2606 6"]
married_select = ["ALL", "YES", "NO"]
type_size_select = ["ALL", "SMALL", "MEDIUM", "LARGE", "FLAGSHIP", "ESCORT", "SUB"]
# Some countries have different navy name in different times; for simplicity, only keep the last one
# The index of country name matches json data, so DO NOT CHANGE the order
country_select = ["ALL", "JP | 大日本帝国海軍", "DE | Bundesmarine", "GB | Royal Navy", "US | United States Navy",
                  "IT | Regia Marina", "FR | Marine nationale", "RU | ВМФ СССР", "CN | 中国人民解放军海军",
                  "", "", "TR | Türk Deniz Kuvvetleri", "NL | Koninklijke Marine", "SE | Svenska marinen",
                  "TH | กองทัพเรือ",
                  "AU | Royal Australian Navy", "CA | Royal Canadian Navy", "MN | Монгол улсын цэргийн",
                  "IS | Landhelgisgæsla Íslands", "CL | Armada de Chile", "FI | Merivoimat", "PL | Marynarka Wojenna",
                  "AH | K.u.K. Kriegsmarine", "GR | Πολεμικό Ναυτικό", "ES | Armada Española"]
flagships = ['BB', 'BBV', 'BC', 'BBG', 'CB', 'CV', 'AV', 'ASDG']
escorts = ['CVL', 'CA', 'CL', 'CLT', 'CAV', 'BM', 'DD', 'AADG', 'AP']
subs = ['SS', 'SC', 'SSV']
# Whenever changed `_header`, double check hardcoding columns
header = ["", "Name", "ID", "Class", "Speed",
          "Range", "Lv.", "HP", "FP", "Armor",
          "Torp.", "Acc.", "Eva.", "LOS", "AA",
          "AS", "Luck", "Fuel", "Ammo.", "Baux.",
          "Slot", "Equip.", "", "", "",
          "Tact.", "", ""]
equip_header = ['Name', 'Amount', 'Specification', 'Description']
range_to_int = {"XL": 4, "L": 3, "M": 2, "S": 1}
range_to_str = {4: "X-Long", 3: "Long", 2: "Medium", 1: "Short"}

equip_spec = {
    'hp': 'HP',
    'atk': 'Firepower',
    'def': 'Armor',
    'torpedo': 'Torpedo',
    'antisub': 'AS',
    'radar': 'LOS',
    'hit': 'Accuracy',
    'range': 'Range',
    'miss': 'Evasion',
    'luck': 'Luck',
    'airDef': 'AA (Ground)',
    'aircraftAtk': 'AA (Air)',
    'correction': 'Correction',
    'missileTmd': 'Intercept',
    'missileHit': 'Penetration'
}
