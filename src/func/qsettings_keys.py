# MUST follow the following format:
# [CONSTANT_KEY_NAME]: str = ['full form of QSettings key identifier'] # [stored datatype]; [comments (optional)]

CONN_SESS_RTY: str = 'CONNECTION/session_retries'  # int
CONN_SESS_SLP: str = 'CONNECTION/session_sleep'  # int
CONN_API_RTY: str = 'CONNECTION/api_retries'  # int
CONN_API_SLP: str = 'CONNECTION/api_sleep'  # int
CONN_THER_RTY: str = 'CONNECTION/thermopylae_retries'  # int

GAME_RANDOM_SEED: str = 'GAME/random_seed'  # int
GAME_SPD_LO: str = 'GAME/speed_lo_bound'  # int
GAME_SPD_HI: str = 'GAME/speed_hi_bound'  # int

LOGIN: str = 'LOGIN'  # bool
LOGIN_AUTO: str = 'LOGIN/auto'  # bool
LOGIN_SAVE: str = 'LOGIN/save'  # bool
LOGIN_USER: str = 'LOGIN/username'  # str
LOGIN_PSWD: str = 'LOGIN/password'  # byte
LOGIN_SERVER: str = 'LOGIN/server_text'  # str
LOGIN_PLATFORM: str = 'LOGIN/platform_text'  # str
LOGIN_DISCLAIMER: str = 'LOGIN/disclaimer'  # bool

STYLE: str = 'style'  # str

UI_MAIN: str = 'UI/remember_resolution'  # bool
UI_MAIN_W: str = 'UI/main_window_width'  # int
UI_MAIN_H: str = 'UI/main_window_height'  # int
UI_MAIN_POS: str = 'UI/main_window_position'  # QPoint
UI_SIDEDOCK: str = 'UI/init_side_dock'  # bool
UI_SIDEDOCK_POS: str = 'UI/side_dock_pos'  # int

THER_BOSS_RTY: str = 'THER/bosses_retries'  # list of int
THER_BOSS_STD: str = 'THER/bosses_retry_standard'  # list of int
THER_TKT_AUTO: str = 'THER/ticket_auto_buy'  # bool
THER_TKT_RSC: str = 'THER/ticket_resource_type'  # str(int); use one F/A/S/B resource to buy
THER_REPAIRS: str = 'THER/repair_levels'  # list of int
THER_HABA_REROLL: str = 'THER/habakkuk_reroll'  # int; in Ex6-3-A1, use Habakkuk skill until desired amount of SS is achieved
THER_SHIP_STARS: str = 'THER/user_ship_stars'  # dict; ship-id (int) to star (int), to keep track of user ship stars
THER_DD: str = 'THER/escort_destroyer_list'  # list of int; len=2 ship ids
THER_CV: str = 'THER/escort_carrier_list'  # list of int; len=1, ship ids
THER_SS: str = 'THER/battle_submarines'  # list of int; len=6, ship ids

EXP_AUTO: str = 'EXP/auto_expedition'  # bool

UI_TAB_ADV: str = 'UI/TAB/advance'  # bool
UI_TAB_EXP: str = 'UI/TAB/expedition'  # bool
UI_TAB_SHIP: str = 'UI/TAB/ship'  # bool
UI_TAB_THER: str = 'UI/TAB/thermopylae'  # bool
