SHIP_TYPE = {
    1: "CV", 2: "CVL", 3: "AV", 4: "BB", 5: "BBV",
    6: "BC", 7: "CA", 8: "CAV", 9: "CLT", 10: "CL",
    11: "BM", 12: "DD", 13: "SSV", 14: "SS", 15: "SC",
    16: "AP", 23: "ASDG", 24: "AADG", 26: "CB", 27: "BBG"
}
RANGE_TYPE = {1: "S", 2: "M", 3: "L", 4: "XL"}
AIR_CONTROL = {1: "Air Supremacy", 2: "Air Superiority", 3: "Air Parity", 4: "Air Denial", 5: "Air Incapability"}
FORMATION = {1: "单纵 LineAhead", 2: "复纵 DoubleLine", 3: "轮形 Diamond", 4: "T形 Echelon", 5: "单横 LineAbreast"}
WAR_EVALUATION = ['-', 'SS', 'S', 'A', 'B', 'C', 'D']
BUILD_TYPE = {1: "Type S.", 2: "Type M.", 3: "Type L.", 4: "?", 5: "?"}


def get_build_type(build_id: int) -> str:
    return BUILD_TYPE[build_id]


def get_combat_formation(formation_id: int) -> str:
    return FORMATION[formation_id]


def get_ship_type(ship_type_id: int) -> str:
    return SHIP_TYPE[ship_type_id]


def get_all_ship_types() -> dict:
    return SHIP_TYPE


def get_ship_los(range_id: int) -> str:
    return RANGE_TYPE[range_id]


def get_war_evaluation(idx: int) -> str:
    return WAR_EVALUATION[idx]

# End of File