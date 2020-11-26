# Whenever changed following options, double check proxy model
lock_select = ["ALL", "YES", "NO"]
level_select = ["ALL", "Lv. 1", "> Lv. 1", "\u2265 Lv. 90", "\u2265 Lv. 100", "= Lv. 110"]
value_select = ["Curr. (w/ Equip.)", "Max. (w/ Equip.)", "Raw (w/o Equip.)"]
mod_select = ["ALL", "Non-mod.", "Mod. I"]
rarity_select = ["\u2606 1", "\u2606 2", "\u2606 3", "\u2606 4", "\u2606 5", "\u2606 6"]
married_select = ["ALL", "Married Only", "Non Married Only"]
size_select = ["ALL", "SMALL", "MEDIUM", "LARGE"]
# TODO: country select, zhuli-huwei
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