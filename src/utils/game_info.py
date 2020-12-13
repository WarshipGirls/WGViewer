SHIP_TYPE = {
    1: "CV", 2: "CVL", 3: "AV", 4: "BB", 5: "BBV",
    6: "BC", 7: "CA", 8: "CAV", 9: "CLT", 10: "CL",
    11: "BM", 12: "DD", 13: "SSV", 14: "SS", 15: "SC",
    16: "AP", 23: "ASDG", 24: "AADG", 26: "CB", 27: "BBG",
    # Enemy types
    17: "Fortess", 99: "Flagship"
}
RANGE_TYPE = {0: "?", 1: "S", 2: "M", 3: "L", 4: "XL"}
AIR_CONTROL = {1: "Air Supremacy", 2: "Air Superiority", 3: "Air Parity", 4: "Air Denial", 5: "Air Incapability"}
FORMATION = {1: "单纵 LineAhead", 2: "复纵 DoubleLine", 3: "轮形 Diamond", 4: "T形 Echelon", 5: "单横 LineAbreast"}
WAR_EVALUATION = ['-', 'SS', 'S', 'A', 'B', 'C', 'D']
BUILD_TYPE = {1: "Type S.", 2: "Type M.", 3: "Type L.", 4: "?", 5: "?"}
# This one is not 100% confirmed (I assumed from challenge['warType'])
COURSEHEADING_TYPE = {1: 'Parallel', 2: 'Heading', 3: 'T+', 4: 'T-'}


def get_heading_type(heading_id: int) -> str:
    try:
        res = COURSEHEADING_TYPE[heading_id]
    except KeyError:
        res = str(heading_id)
    return res


def get_build_type(build_id: int) -> str:
    try:
        res = BUILD_TYPE[build_id]
    except KeyError:
        res = str(build_id)
    return res


def get_combat_formation(formation_id: int) -> str:
    try:
        res = FORMATION[formation_id]
    except KeyError:
        res = str(formation_id)
    return res


def get_ship_type(ship_type_id: int) -> str:
    try:
        res = SHIP_TYPE[ship_type_id]
    except KeyError:
        res = str(ship_type_id)
    return res


def get_all_ship_types() -> dict:
    return SHIP_TYPE


def get_ship_los(range_id: int) -> str:
    try:
        res = RANGE_TYPE[range_id]
    except KeyError:
        res = str(range_id)
    return res


def get_war_evaluation(idx: int) -> str:
    try:
        res = WAR_EVALUATION[idx]
    except KeyError:
        res = str(idx)
    return res

# End of File
