from math import ceil


def get_repair_type(ship_info: dict) -> int:
    curr_hp = ship_info['battleProps']['hp']
    max_hp = ship_info['battlePropsMax']['hp']
    res = -1
    if curr_hp < max_hp:
        # slightly damaged
        res = 0
    elif curr_hp < ceil(max_hp * 0.5):
        # moderately damaged
        res = 1
    elif curr_hp < ceil(max_hp * 0.25):
        # heavily damaged
        res = 2
    elif curr_hp < 0:
        # sunken
        res = 3
    else:
        pass
    return res


def process_spy_json(spy_json: dict, all_equipment: [dict, None] = None) -> str:
    enemy_info = spy_json['enemyVO']
    detect_result = "success" if enemy_info['isFound'] == 1 else "fail"
    detect_rate = enemy_info['successRate']
    spy_out = f"==== Detection {detect_result} ===="
    if enemy_info['canSkip'] == 1:
        spy_out += f"Terrain Avoidance with success rate = {detect_rate}%"
    spy_out += "\n"
    enemy_fleet = enemy_info['enemyFleet']
    spy_out += f"{enemy_fleet['title']} | {get_combat_formation(int(enemy_fleet['formation']))}"
    spy_out += "\n"
    enemy_ships = enemy_info['enemyShips']
    for e in enemy_ships:
        e_str = "{:<12s} Lv.{:<4d} {}".format(e['title'], e['level'], get_ship_type(e['type']))
        e_str += "\n"
        e_str += "HP {:4s} ATK {:4s} DEF {:4s} TPD {:4s} EVA {:4s}".format(str(e['hp']), str(e['atk']), str(e['def']), str(e['torpedo']), str(e['miss']))
        e_str += "\n"
        e_str += "AA {:4s} AS  {:4s} SPD {:4s} LOS {:4s} RNG {:4s}".format(str(e['airDef']), str(e['antisub']), str(e['speed']), str(e['radar']),
                                                                           get_ship_los(e['range']))
        e_str += "\n"
        if all_equipment is None:
            pass
        else:
            for q in e['equipment']:
                if isinstance(q, int) is False or q == 0:
                    continue
                _e = next((i for i in all_equipment if i['cid'] == q))
                e_str += "{} ".format(_e['title'])
            e_str += "\n"
        spy_out += e_str
    return spy_out


if __name__ == "__main__":
    from src.utils.game_info import (
        get_combat_formation, get_ship_type, get_ship_los
    )
else:
    from .game_info import (
        get_combat_formation, get_ship_type, get_ship_los
    )

# End of File