# Whenever changed following options, double check proxy model
lock_select = ["ALL", "YES", "NO"]
level_select = ["ALL", "Lv. 1", "> Lv. 1", "\u2265 Lv. 90", "\u2265 Lv. 100", "= Lv. 110"]
value_select = ["Curr. (w/ Equip.)", "Max. (w/ Equip.)", "Raw (w/o Equip.)"]
mod_select = ["ALL", "Non-mod.", "Mod. I"]
rarity_select = ["ALL", "\u2606 1", "\u2606 2", "\u2606 3", "\u2606 4", "\u2606 5", "\u2606 6"]
married_select = ["ALL", "YES", "NO"]
type_size_select = ["ALL", "SMALL", "MEDIUM", "LARGE", "FLAGSHIP", "ESCORT", "SUB"]
country_select = ["ALL", "JP | 大日本帝国海軍","DE | Kaiserliche Marine/Kriegsmarine/Bundesmarine","GB | Royal Navy","US | United States Navy",
"IT | Regia Marina","FR | Marine nationale française","RU | Российский императорский флот/Военно-морской флот СССР","CN | 中华民国海军/中国人民解放军海军",
"","","TR | Türk Deniz Kuvvetleri","NL | Koninklijke Marine","SE | Svenska marinen","TH | กองทัพเรือ",
"AU | Royal Australian Navy","CA | Royal Canadian Navy - Marine Royale Canadienne","MN | Монгол улсын цэргийн",
"IS | Landhelgisgæsla Íslands","CL | Armada de Chile","FI | Merivoimat","PL | Okręt Rzeczypospolitej Polskiej",
"AH | Kaiserliche und königliche Kriegsmarine","GR | Πολεμικό Ναυτικό","ES | Armada Española"]
flagships = ['BB', 'BBV', 'BC', 'BBG', 'CB', 'CV', 'AV', 'ASDG']
escorts = ['CVL', 'CA', 'CL', 'CLT', 'CAV', 'BM', 'DD', 'AADG', 'AP']
subs = ['SS', 'SC', 'SSV']
# Whenever changed `_header`, double check hardcoding columns
_header = [ "", "Name", "ID", "Class", "Speed",
            "Range", "Lv.", "HP", "FP", "Armor",
            "Torp.", "Acc.", "Eva.", "LOS", "AA",
            "AS", "Luck", "Fuel", "Ammo.", "Baux.",
            "Slot", "Equip.", "", "", "",
            "Tact.", "", ""]
_equip_header = ['Name', 'Amount', 'Specification', 'Description']
_range_to_int = {"XL": 4, "L": 3, "M": 2, "S": 1}
_range_to_str = {4: "X-Long", 3: "Long", 2: "Medium", 1: "Short"}


# {
# 1:"JP | 大日本帝国海軍",
# 2:"DE | Kaiserliche Marine/Kriegsmarine/Bundesmarine",
# 3:"GB | Royal Navy",
# 4:"US | United States Navy",
# 5:"IT | Regia Marina",
# 6:"FR | Marine nationale française",
# 7:"RU | Российский императорский флот/Военно-морской флот СССР",
# 8:"CN | 中华民国海军/中国人民解放军海军",
# 9:"???",
# 10:"Enemy",
# 11:"TR | Türk Deniz Kuvvetleri",
# 12:"NL | Koninklijke Marine",
# 13:"SE | Svenska marinen",
# 14:"TH | กองทัพเรือ",
# 15:"AU | Royal Australian Navy",
# 16:"CA | Royal Canadian Navy - Marine Royale Canadienne",
# 17:"MN | Монгол улсын цэргийн",
# 18:"IS | Landhelgisgæsla Íslands",
# 19:"CL | Armada de Chile",
# 20:"FI | Merivoimat",
# 21:"PL | Okręt Rzeczypospolitej Polskiej",
# 22:"AH | Kaiserliche und königliche Kriegsmarine",
# 23:"GR | Πολεμικό Ναυτικό",
# 24:"ES | Armada Española",
# "0":"Enemy",
# }

_equip_spec = {
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