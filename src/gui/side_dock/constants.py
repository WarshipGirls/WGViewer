CSV_HEADER: list = ['TS', 'Fuel', 'Ammo.', 'Steel', 'Baux.', 'Gold', 'Repair', 'Build', 'BP_Constr', 'BP_Dev', 'Revive', 'DD', 'CA', 'BB', 'CV', 'SS']
CSV_FILENAME: str = 'resource_log.csv'
CSV_LOG_COUNTDOWN: int = 900  # seconds
CSV_LOG_TIMER_INTERVAL: int = 60000  # micro-seconds
TASK_TYPE: dict = {'1': "SINGLE", '2': "DAILY", '3': "WEEKLY", '4': "LIMITED TIME"}

BATH_LABEL_L: str = 'Repairing Dock Locked'
BATH_LABEL_R: str = ''
BLD_LABEL_L: str = 'Constr. Slot'
BLD_LABEL_R: str = 'Locked'
DEV_LABEL_L: str = 'Dev. Slot'
DEV_LABEL_R: str = 'Locked'
EXP_LABEL_L: str = 'Exped. Fleet'
EXP_LABEL_R: str = 'Idling'
