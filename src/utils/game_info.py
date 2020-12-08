from src.func import constants as CONST


def get_combat_formation(formation: int) -> str:
    return CONST.formation[formation]


def get_ship_type(ship_type_id: int) -> str:
    return CONST.ship_type[ship_type_id]


def get_ship_los(range_id: int) -> str:
    return CONST.range_type[range_id]

# End of File
