# TODO As of now, the function names are added manually, is there a more efficient way?
#   - a slightly faster way is import file_name and do dir(file_name), then manually copy paste
#   - Or I could write a script...

from .getInitConfigs import save_init_data

from .path import (
    get_init_dir, get_user_dir, get_temp_dir,
    clear_cache_folder,
)

from .qsettings import (
    get_color_scheme, get_qsettings_file, get_key_path,
    is_key_exists, _del_key_file
)

from .json import (
    get_equipmentVo, get_processed_userShipVo, get_pveExploreVo,
    get_shipCard, get_shipEquipmnt, get_shipItem, get_tactics_json, get_userVo, get_user_fleets, get_user_tactics,
    save_equipmentVo, save_processed_userShipVo, save_pveExploreVo, save_userVo, save_user_fleets, save_user_tactics,
    init_ships_temp
)

from .process import (
    get_big_success_rate, get_exp_fleets,
    get_ship_equips, update_equipment_amount, find_index, find_all_indices
)