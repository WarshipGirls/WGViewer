import logging
import random

from time import time
from typing import List, Union

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QFont, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel, QLineEdit, QSpinBox

from src.utils import repair_id_to_text, repair_text_to_id
from src.func import qsettings_keys as QKEYS
from src.gui.custom_widgets import QHLine

HEADER1: int = 20
HEADER2: int = 15
HEADER3: int = 12


def create_qcombobox(choices: list, idx: int = 0) -> QComboBox:
    c = QComboBox()
    c.addItems(choices)
    c.setCurrentIndex(idx)
    return c


def create_qlabel(text: str, font_size: int = -1) -> QLabel:
    l = QLabel()
    l.setText(text)
    if font_size != -1:
        font = QFont('consolas', font_size)
    else:
        font = QFont('consolas')
    font.setBold(True)
    l.setFont(font)
    return l


def create_qlineedit(default: int, max_len: int) -> QLineEdit:
    q = QLineEdit()
    q.setPlaceholderText(str(default))
    q.setMaxLength(max_len)
    q.setValidator(get_int_mask())
    return q


def create_qspinbox(default: int, min_val: int, max_val: int, step: int = 1) -> QSpinBox:
    q = QSpinBox()
    q.setValue(default)
    q.setMinimum(min_val)
    q.setMaximum(max_val)
    q.setSingleStep(step)
    return q


def get_int_mask() -> QRegExpValidator:
    return QRegExpValidator(QRegExp("[1-9][0-9]*"))


class SettingsTemplate(QWidget):
    def __init__(self, qsettings):
        super().__init__()
        self.qsettings = qsettings
        self.layout = QGridLayout()
        # Lesson: without setLayout(), it only renders the last QWidget
        self.setLayout(self.layout)

        # Lession: QWidget created in __init__ will be auto put in the layout
        #   - workaround: use addWidget() later to move it; or pre-set with None
        self.h_line = None

    def set_h_line(self) -> None:
        self.h_line = QHLine(parent=self, color=QColor(0, 0, 0), width=10)

    def init_hack(self, row: int) -> None:
        # following is a hack; TODO: setRowStretch is not working properly
        for h in range(10):
            row += 1
            self.layout.addWidget(QLabel(""), row, 0, 1, 4)

    def init_checkbox(self, res, name: str) -> None:
        self.qsettings.setValue(name, (res == 2))

    def init_dropdown(self, dropdown: QComboBox, key: str, default_idx: int) -> None:
        if self.qsettings.contains(key) is True:
            dropdown.setCurrentIndex(self.qsettings.value(key, type=int))
        else:
            dropdown.setCurrentIndex(default_idx)

    def set_checkbox_status(self, ck: QCheckBox, key: str, default: bool = True) -> None:
        if self.qsettings.contains(key) is True:
            ck.setChecked(self.qsettings.value(key, type=bool) is True)
        else:
            ck.setChecked(default)


class UISettings(SettingsTemplate):

    def __init__(self, qsettings):
        super().__init__(qsettings)
        self.side_dock = QCheckBox("Navy Base Overview", self)
        self.side_dock_pos = create_qcombobox(['Right', 'Left'])

        self.tab_adv = QCheckBox("Advance Functions", self)
        self.tab_exp = QCheckBox("Expedition", self)
        self.tab_ship = QCheckBox("Dock", self)
        self.tab_ther = QCheckBox("Thermopylae", self)

        self.init_ui()

    def init_ui(self) -> None:
        row = 0
        self.set_h_line()
        row = self.init_side_dock(row)
        row = self.init_tabs(row)
        self.init_hack(row)

    def handle_sidedock(self):
        self.qsettings.setValue(QKEYS.UI_SIDEDOCK, self.side_dock.isChecked())
        self.side_dock_pos.setEnabled(self.side_dock.isChecked())

    def init_side_dock(self, row: int) -> int:
        self.layout.addWidget(create_qlabel(text="ON START", font_size=HEADER2), row, 0, 1, 4)

        row += 1
        self.layout.addWidget(create_qlabel(text="SIDE DOCK", font_size=HEADER3), row, 0, 1, 4)
        row += 1
        self.layout.addWidget(self.h_line, row, 0, 1, 4)
        row += 1
        self.set_checkbox_status(self.side_dock, QKEYS.UI_SIDEDOCK)
        self.side_dock.stateChanged.connect(self.handle_sidedock)
        self.layout.addWidget(self.side_dock, row, 0)
        self.init_dropdown(self.side_dock_pos, QKEYS.UI_SIDEDOCK_POS, 0)
        self.side_dock_pos.setToolTip("Set the default position of side dock")
        self.side_dock_pos.setEnabled(self.side_dock.isChecked())
        self.side_dock_pos.currentIndexChanged.connect(lambda _: self.qsettings.setValue(QKEYS.UI_SIDEDOCK_POS, self.side_dock_pos.currentIndex()))
        self.layout.addWidget(self.side_dock_pos, row, 1)
        return row

    def init_tabs(self, row: int) -> int:
        row += 1
        self.layout.addWidget(create_qlabel(text="TABS", font_size=12), row, 0, 1, 4)
        row += 1
        self.layout.addWidget(self.h_line, row, 0, 1, 4)
        row += 1

        self.set_checkbox_status(self.tab_adv, QKEYS.UI_TAB_ADV)
        self.set_checkbox_status(self.tab_exp, QKEYS.UI_TAB_EXP)
        self.set_checkbox_status(self.tab_ship, QKEYS.UI_TAB_SHIP)
        self.set_checkbox_status(self.tab_ther, QKEYS.UI_TAB_THER)
        self.tab_adv.stateChanged.connect(lambda res: self.init_checkbox(res, QKEYS.UI_TAB_ADV))
        self.tab_exp.stateChanged.connect(lambda res: self.init_checkbox(res, QKEYS.UI_TAB_EXP))
        self.tab_ship.stateChanged.connect(lambda res: self.init_checkbox(res, QKEYS.UI_TAB_SHIP))
        self.tab_ther.stateChanged.connect(lambda res: self.init_checkbox(res, QKEYS.UI_TAB_THER))
        self.layout.addWidget(self.tab_adv, row, 0)
        self.layout.addWidget(self.tab_exp, row, 1)
        self.layout.addWidget(self.tab_ship, row, 2)
        self.layout.addWidget(self.tab_ther, row, 3)
        return row

    def on_reset(self) -> None:
        self.side_dock_pos.setCurrentIndex(0)
        self.qsettings.setValue(QKEYS.UI_SIDEDOCK_POS, 0)
        # If this gets bigger, use a group or container
        self.side_dock.setChecked(True)
        self.tab_adv.setChecked(True)
        self.tab_exp.setChecked(True)
        self.tab_ship.setChecked(True)
        self.tab_ther.setChecked(True)
        self.qsettings.setValue(QKEYS.UI_SIDEDOCK, True)
        self.qsettings.setValue(QKEYS.UI_TAB_ADV, True)
        self.qsettings.setValue(QKEYS.UI_TAB_EXP, True)
        self.qsettings.setValue(QKEYS.UI_TAB_SHIP, True)
        self.qsettings.setValue(QKEYS.UI_TAB_THER, True)


class GameSettings(SettingsTemplate):
    def __init__(self, qsettings):
        super().__init__(qsettings)
        for col in range(5):
            self.layout.setColumnStretch(col, 1)

        _d = self.get_init_value(QKEYS.GAME_RANDOM_SEED)
        self.seed_input = create_qlineedit(default=_d, max_len=16)
        self.speed_lo_input = None
        self.speed_hi_input = None
        self.session_retries = None
        self.session_sleep = None
        self.api_retries = None
        self.api_sleep = None
        self.ther_boss_retry = None

        self.init_ui()

    def init_ui(self):
        row = 0
        self.set_h_line()
        row = self.init_overall(row)
        row = self.init_connections(row)
        row = self.init_thermopylae(row)
        self.init_hack(row)

    def init_overall(self, row: int) -> int:
        self.layout.addWidget(create_qlabel(text='Overall', font_size=HEADER2), row, 0)
        row += 1
        self.layout.addWidget(self.h_line, row, 0, 1, 5)

        row += 1
        self.layout.addWidget(create_qlabel(text='Random Seed'), row, 0)
        self.seed_input.textChanged.connect(self.set_random_seed)
        self.layout.addWidget(self.seed_input, row, 1)

        row += 1
        speed_label = create_qlabel(text='Game Speed (sec)')
        speed_label.setToolTip("Set server request intervals.\nInvalid inputs will be ignored (such as low > high)")
        self.layout.addWidget(speed_label, row, 0)
        self.layout.addWidget(create_qlabel('Lower Bound'), row, 1)
        _d = self.get_init_value(QKEYS.GAME_SPD_LO)
        self.speed_lo_input = create_qspinbox(_d, 5, 999)
        self.speed_lo_input.valueChanged.connect(lambda res: self.create_input(res, self.speed_lo_input, _d, QKEYS.GAME_SPD_LO))
        self.layout.addWidget(self.speed_lo_input, row, 2)
        self.layout.addWidget(create_qlabel('Upper Bound'), row, 3)
        _d = self.get_init_value(QKEYS.GAME_SPD_HI)
        self.speed_hi_input = create_qspinbox(_d, 10, 999)
        self.speed_hi_input.valueChanged.connect(lambda res: self.create_input(res, self.speed_hi_input, _d, QKEYS.GAME_SPD_HI))
        self.layout.addWidget(self.speed_hi_input, row, 4)
        return row

    def init_connections(self, row: int) -> int:
        row += 1
        self.layout.addWidget(create_qlabel(text='Connection', font_size=HEADER2), row, 0)
        row += 1
        self.layout.addWidget(self.h_line, row, 0, 1, 5)

        row += 1
        self.layout.addWidget(create_qlabel(text='Retry Limit', font_size=HEADER3), row, 0)
        self.layout.addWidget(create_qlabel(text='session'), row, 1)
        _d = self.get_init_value(QKEYS.CONN_SESS_RTY)
        self.session_retries = create_qspinbox(_d, 1, 99)
        self.session_retries.valueChanged.connect(lambda res: self.create_input(res, self.session_retries, _d, QKEYS.CONN_SESS_RTY))
        self.layout.addWidget(self.session_retries, row, 2)
        self.layout.addWidget(create_qlabel(text='sleep (sec)'), row, 3)
        _d = self.get_init_value(QKEYS.CONN_SESS_SLP)
        self.session_sleep = create_qspinbox(_d, 1, 99)
        self.session_sleep.valueChanged.connect(lambda res: self.create_input(res, self.session_sleep, _d, QKEYS.CONN_SESS_SLP))
        self.layout.addWidget(self.session_sleep, row, 4)

        row += 1
        self.layout.addWidget(create_qlabel(text='WGR API'), row, 1)
        _d = self.get_init_value(QKEYS.CONN_API_RTY)
        self.api_retries = create_qspinbox(_d, 1, 99)
        self.api_retries.valueChanged.connect(lambda res: self.create_input(res, self.api_retries, _d, QKEYS.CONN_API_RTY))
        self.layout.addWidget(self.api_retries, row, 2)
        self.layout.addWidget(create_qlabel(text='sleep (sec)'), row, 3)
        _d = self.get_init_value(QKEYS.CONN_API_SLP)
        self.api_sleep = create_qspinbox(_d, 1, 99)
        self.api_sleep.valueChanged.connect(lambda res: self.create_input(res, self.api_sleep, _d, QKEYS.CONN_API_SLP))
        self.layout.addWidget(self.api_sleep, row, 4)
        return row

    def init_thermopylae(self, row: int) -> int:
        row += 1
        self.layout.addWidget(create_qlabel(text='Thermopylae'), row, 1)
        _d = self.get_init_value(QKEYS.CONN_THER_RTY)
        self.ther_boss_retry = create_qspinbox(_d, 1, 9)
        self.ther_boss_retry.valueChanged.connect(lambda res: self.create_input(res, self.ther_boss_retry, _d, QKEYS.CONN_THER_RTY))
        self.layout.addWidget(self.ther_boss_retry, row, 2)
        row += 1

        return row

    def on_reset(self) -> None:
        t = str(self.get_init_value(QKEYS.GAME_RANDOM_SEED, True))
        self.seed_input.setText(t)
        self.qsettings.setValue(QKEYS.GAME_RANDOM_SEED, t)
        t = self.get_init_value(QKEYS.GAME_SPD_LO, True)
        self.speed_lo_input.setValue(t)
        self.qsettings.setValue(QKEYS.GAME_SPD_LO, t)
        t = self.get_init_value(QKEYS.GAME_SPD_HI, True)
        self.speed_hi_input.setValue(t)
        self.qsettings.setValue(QKEYS.GAME_SPD_HI, t)
        t = self.get_init_value(QKEYS.CONN_SESS_RTY, True)
        self.session_retries.setValue(t)
        self.qsettings.setValue(QKEYS.CONN_SESS_RTY, t)
        t = self.get_init_value(QKEYS.CONN_SESS_SLP, True)
        self.session_sleep.setValue(t)
        self.qsettings.setValue(QKEYS.CONN_SESS_SLP, t)
        t = self.get_init_value(QKEYS.CONN_API_RTY, True)
        self.api_retries.setValue(t)
        self.qsettings.setValue(QKEYS.CONN_API_RTY, t)
        t = self.get_init_value(QKEYS.CONN_API_SLP, True)
        self.api_sleep.setValue(t)
        self.qsettings.setValue(QKEYS.CONN_API_SLP, t)
        t = self.get_init_value(QKEYS.CONN_THER_RTY, True)
        self.ther_boss_retry.setValue(t)
        self.qsettings.setValue(QKEYS.CONN_THER_RTY, t)

    def create_input(self, _input: str, _edit: Union[QLineEdit, QSpinBox], _default: int, _field: str) -> None:
        if _input == '':
            _input = _default
            _edit.setPlaceholderText(str(_default))
        else:
            pass
        self.qsettings.setValue(_field, _input)

    def get_init_value(self, field: str, is_default: bool = False) -> int:
        if (self.qsettings.contains(field) is True) and (is_default is False):
            d = self.qsettings.value(field, type=int)
        else:
            if field == QKEYS.GAME_RANDOM_SEED:
                d = 42
            elif field == QKEYS.GAME_SPD_LO:
                d = 5
            elif field == QKEYS.GAME_SPD_HI:
                d = 10
            elif field == QKEYS.CONN_SESS_RTY:
                d = 5
            elif field == QKEYS.CONN_SESS_SLP:
                d = 3
            elif field == QKEYS.CONN_API_RTY:
                d = 5
            elif field == QKEYS.CONN_API_SLP:
                d = 3
            elif field == QKEYS.CONN_THER_RTY:
                d = 3
            else:
                d = 5
                logging.error(f"Unsupported QKEYS filed {field}")
        return d

    def set_random_seed(self, _input: str) -> None:
        random_seed = time() if _input == '' else _input
        random.seed(int(random_seed))
        self.qsettings.setValue(QKEYS.GAME_RANDOM_SEED, int(_input))


class TabsSettings(SettingsTemplate):
    def __init__(self, qsettings):
        super().__init__(qsettings)
        for col in range(5):
            self.layout.setColumnStretch(col, 1)

        self.ther_ticket_auto = QCheckBox("Auto Purchase", self)
        self.ther_ticket_resource = create_qcombobox(['Fuel', 'Ammunition', 'Steel', 'Bauxite'])

        _d = self.get_init_value(QKEYS.THER_BOSS_RTY)
        self.ther_boss_retry: List[QSpinBox] = [
            create_qspinbox(int(_d[0]), 0, 9),
            create_qspinbox(int(_d[1]), 0, 9),
            create_qspinbox(int(_d[2]), 0, 9)
        ]
        _d = self.get_init_value(QKEYS.THER_BOSS_STD)
        self.ther_boss_std: List[QSpinBox] = [
            create_qspinbox(int(_d[0]), 0, 6),
            create_qspinbox(int(_d[1]), 0, 6),
            create_qspinbox(int(_d[2]), 0, 6)
        ]
        repair_choices = ['Slightly Damaged', 'Moderately Damaged', 'Heavily Damaged']
        # Lesson: cannot use list = [func()] * 6, that would duplicate instance rather make six calls
        self.ther_repairs: List[QComboBox] = [
            create_qcombobox(repair_choices, 1),
            create_qcombobox(repair_choices, 1),
            create_qcombobox(repair_choices, 1),
            create_qcombobox(repair_choices, 1),
            create_qcombobox(repair_choices, 1),
            create_qcombobox(repair_choices, 1),
        ]

        self.init_ui()

    def init_ui(self):
        row = 0
        row = self.init_thermopylae(row)
        self.init_hack(row)

    def handle_auto_ticket(self):
        self.qsettings.setValue(QKEYS.THER_TKT_AUTO, (self.ther_ticket_auto.isChecked()))
        self.ther_ticket_resource.setEnabled(self.ther_ticket_auto.isChecked())

    def init_thermopylae(self, row: int) -> int:
        self.layout.addWidget(create_qlabel(text='Thermopylae', font_size=HEADER3), row, 0)
        self.layout.addWidget(create_qlabel(text='Tickets'), row, 1)
        self.set_checkbox_status(self.ther_ticket_auto, QKEYS.THER_TKT_AUTO)
        self.ther_ticket_auto.stateChanged.connect(self.handle_auto_ticket)
        self.layout.addWidget(self.ther_ticket_auto, row, 2)
        self.layout.addWidget(create_qlabel(text='With'), row, 3)
        self.init_dropdown(self.ther_ticket_resource, QKEYS.THER_TKT_RSC, 3)
        self.ther_ticket_resource.currentIndexChanged.connect(lambda _: self.qsettings.setValue(QKEYS.THER_TKT_RSC, self.ther_ticket_resource.currentIndex()))
        self.ther_ticket_resource.setEnabled(self.ther_ticket_auto.isChecked())
        self.layout.addWidget(self.ther_ticket_resource, row, 4)

        row += 1
        self.layout.addWidget(create_qlabel(text='Bosses Retries'), row, 1)
        tbr_init = self.get_init_value(QKEYS.THER_BOSS_RTY)
        for i in range(3):
            self.ther_boss_retry[i].valueChanged.connect(lambda res, _i=i: self.create_input(res, self.ther_boss_retry[_i], tbr_init, _i, QKEYS.THER_BOSS_RTY))
            self.layout.addWidget(self.ther_boss_retry[i], row, i+2)

        row += 1
        ther_boss_retry_std_label = create_qlabel(text='On Sunken')
        ther_boss_retry_std_label.setToolTip("Sunken at least how many enemies to disable boss re-fight")
        self.layout.addWidget(ther_boss_retry_std_label, row, 1)
        tbs_init = self.get_init_value(QKEYS.THER_BOSS_STD)
        for i in range(3):
            self.ther_boss_std[i].valueChanged.connect(lambda res, _i=i: self.create_input(res, self.ther_boss_std[_i], tbs_init, _i, QKEYS.THER_BOSS_STD))
            self.layout.addWidget(self.ther_boss_std[i], row, i+2)

        row += 1
        ther_repair_levels_label = create_qlabel(text='Fleet Repair Levels')
        ther_repair_levels_label.setToolTip("Set the repair levels for battle fleet\n1st row:\t#1 #2 #3\n2nd row:\t#4 #5 #6")
        self.layout.addWidget(ther_repair_levels_label, row, 1)
        tbp_init = self.get_init_value(QKEYS.THER_REPAIRS)
        for i in range(3):
            self.ther_repairs[i].currentTextChanged.connect(lambda res, _i=i: self.dropdown_input(res, self.ther_repairs[_i], tbp_init, _i, QKEYS.THER_REPAIRS))
            self.layout.addWidget(self.ther_repairs[i], row, i+2)
        row += 1
        for i in range(3, 6):
            self.ther_repairs[i].currentTextChanged.connect(lambda res, _i=i: self.dropdown_input(res, self.ther_repairs[_i], tbp_init, _i, QKEYS.THER_REPAIRS))
            self.layout.addWidget(self.ther_repairs[i], row, i-1)

        row += 1
        return row

    def create_input(self, _input: str, _edit: QSpinBox, _default: list, idx: int, _field: str) -> None:
        # Lesson: locals() shows all arguments https://stackoverflow.com/a/50763376/14561914
        if _input == '':
            save = _default
            _edit.setPlaceholderText(str(_default[idx]))
        else:
            _default[idx] = int(_input)
            save = _default
        self.qsettings.setValue(_field, save)

    def dropdown_input(self, _input: str, _edit: QComboBox, _default: list, idx: int, _field: str) -> None:
        if _input == '':
            save = _default
            _edit.setPlaceholderText(repair_id_to_text(_default[idx]))
        else:
            _default[idx] = repair_text_to_id(_input)
            save = _default
        self.qsettings.setValue(_field, save)

    def on_reset(self) -> None:
        self.ther_ticket_auto.setChecked(True)
        self.qsettings.setValue(QKEYS.THER_TKT_AUTO, True)
        self.ther_ticket_resource.setCurrentIndex(3)
        self.qsettings.setValue(QKEYS.THER_TKT_RSC, 3)

        _d = self.get_init_value(QKEYS.THER_BOSS_RTY, True)
        self.qsettings.setValue(QKEYS.THER_BOSS_RTY, _d)
        for i in range(3):
            self.ther_boss_retry[i].setValue(_d[i])

        _d = self.get_init_value(QKEYS.THER_BOSS_STD, True)
        self.qsettings.setValue(QKEYS.THER_BOSS_STD, _d)
        for i in range(3):
            self.ther_boss_std[i].setValue(_d[i])

        _d = self.get_init_value(QKEYS.THER_REPAIRS, True)
        self.qsettings.setValue(QKEYS.THER_REPAIRS, _d)
        for i in range(6):
            self.ther_repairs[i].setCurrentIndex(1)

    def get_init_value(self, field: str, is_default: bool = False) -> Union[list, int]:
        if (self.qsettings.contains(field) is True) and (is_default is False):
            d = self.qsettings.value(field)
        else:
            if field == QKEYS.THER_BOSS_RTY:
                d = [3, 5, 9]
            elif field == QKEYS.THER_BOSS_STD:
                d = [1, 2, 2]
            elif field == QKEYS.THER_REPAIRS:
                d = [2, 2, 2, 2, 2, 2]
            elif field == QKEYS.THER_TKT_RSC:
                d = 3
            else:
                logging.error(f"Unsupported QKEYS filed {field}")
                d = [1]
        return d

# End of File
