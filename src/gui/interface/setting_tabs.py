import logging
import random

from time import time

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QFont, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel, QLineEdit

from src.func import qsettings_keys as QKEYS
from src.gui.custom_widgets import QHLine

# TODO: repeadted function calls in __init__, init members with None
# TODO: common functions in classes

HEADER1: int = 20
HEADER2: int = 15
HEADER3: int = 12


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


def get_int_mask() -> QRegExpValidator:
    return QRegExpValidator(QRegExp("[1-9][0-9]*"))


class UISettings(QWidget):

    def __init__(self, qsettings):
        super().__init__()
        self.qsettings = qsettings

        self.layout = QGridLayout()
        # Lesson: without setLayout(), it only renders the last QWidget
        self.setLayout(self.layout)

        self.side_dock = QCheckBox("Navy Base Overview", self)
        self.side_dock.stateChanged.connect(self.handle_side_dock_init)
        self.dropdown_side_dock = QComboBox()
        self.dropdown_side_dock.currentTextChanged.connect(self.handle_side_dock_pos)

        self.tab_adv = QCheckBox("Advance Functions", self)
        self.handle_tab_init(self.tab_adv, QKEYS.UI_TAB_ADV)
        self.tab_exp = QCheckBox("Expedition", self)
        self.handle_tab_init(self.tab_exp, QKEYS.UI_TAB_EXP)
        self.tab_ship = QCheckBox("Dock", self)
        self.handle_tab_init(self.tab_ship, QKEYS.UI_TAB_SHIP)
        self.tab_ther = QCheckBox("Thermopylae", self)
        self.handle_tab_init(self.tab_ther, QKEYS.UI_TAB_THER)

        self.init_ui()

    def init_ui(self) -> None:
        row = 0
        row = self.init_side_dock(row)
        row = self.init_tabs(row)
        self.init_hack(row)

    def init_side_dock(self, row: int) -> int:
        header = create_qlabel(text="ON START", font_size=HEADER2)
        self.layout.addWidget(header, row, 0, 1, 4)

        row += 1
        h2 = create_qlabel(text="SIDE DOCK", font_size=HEADER3)
        self.layout.addWidget(h2, row, 0, 1, 4)
        row += 1
        self.layout.addWidget(QHLine(parent=self, color=QColor(0, 0, 0), width=10), row, 0, 1, 4)
        row += 1
        if self.qsettings.value(QKEYS.UI_SIDEDOCK) == 'true':
            self.side_dock.setChecked(False)
        else:
            self.side_dock.setChecked(True)
        self.layout.addWidget(self.side_dock, row, 0, 1, 1)
        self.dropdown_side_dock.setToolTip("Set the default position of side dock")
        self.dropdown_side_dock.addItems(['Right', 'Left'])
        self.layout.addWidget(self.dropdown_side_dock, row, 1, 1, 1)
        return row

    def init_tabs(self, row: int) -> int:
        row += 1
        h3 = create_qlabel(text="TABS", font_size=12)
        self.layout.addWidget(h3, row, 0, 1, 4)
        row += 1
        self.layout.addWidget(QHLine(parent=self, color=QColor(0, 0, 0), width=10), row, 0, 1, 4)
        row += 1
        if self.qsettings.value(QKEYS.UI_TAB_ADV) == 'true':
            self.tab_adv.setChecked(True)
        else:
            self.tab_adv.setChecked(False)

        if self.qsettings.value(QKEYS.UI_TAB_EXP) == 'true':
            self.tab_exp.setChecked(True)
        else:
            self.tab_exp.setChecked(False)

        if self.qsettings.value(QKEYS.UI_TAB_SHIP) == 'true':
            self.tab_ship.setChecked(True)
        else:
            self.tab_ship.setChecked(False)

        if self.qsettings.value(QKEYS.UI_TAB_THER) == 'true':
            self.tab_ther.setChecked(True)
        else:
            self.tab_ther.setChecked(False)
        self.layout.addWidget(self.tab_adv, row, 0, 1, 1)
        self.layout.addWidget(self.tab_exp, row, 1, 1, 1)
        self.layout.addWidget(self.tab_ship, row, 2, 1, 1)
        self.layout.addWidget(self.tab_ther, row, 3, 1, 1)
        return row

    def init_hack(self, row: int) -> None:
        # following is a hack; TODO: setRowStretch is not working properly
        for h in range(10):
            row += 1
            self.layout.addWidget(QLabel(""), row, 0, 1, 4)

    def on_reset(self) -> None:
        # If this gets bigger, use a group or container
        self.side_dock.setChecked(True)
        self.tab_adv.setChecked(True)
        self.tab_exp.setChecked(True)
        self.tab_ship.setChecked(True)
        self.tab_ther.setChecked(True)

    def handle_side_dock_pos(self) -> None:
        if self.dropdown_side_dock.currentText() == 'Right':
            self.qsettings.setValue(QKEYS.UI_SIDEDOCK_POS, 'right')
        elif self.dropdown_side_dock.currentText() == 'Left':
            self.qsettings.setValue((QKEYS.UI_SIDEDOCK_POS, 'left'))
        else:
            self.qsettings.setValue(QKEYS.UI_SIDEDOCK_POS, 'right')

    def handle_side_dock_init(self) -> None:
        if self.side_dock.isChecked() is True:
            self.qsettings.setValue(QKEYS.UI_SIDEDOCK, False)
        else:
            self.qsettings.setValue(QKEYS.UI_SIDEDOCK, True)

    def handle_tab_init(self, cb: QCheckBox, name: str) -> None:
        if cb.isChecked() is True:
            self.qsettings.setValue(name, True)
        else:
            self.qsettings.setValue(name, False)


class GameSettings(QWidget):
    def __init__(self, qsettings):
        super().__init__()
        self.qsettings = qsettings

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        _d = self.get_init_value(QKEYS.GAME_RANDOM_SEED)
        self.seed_input = create_qlineedit(default=_d, max_len=16)
        _d = self.get_init_value(QKEYS.GAME_SPD_LO)
        self.speed_lo_input = create_qlineedit(default=_d, max_len=3)
        _d = self.get_init_value(QKEYS.GAME_SPD_HI)
        self.speed_hi_input = create_qlineedit(default=_d, max_len=3)
        _d = self.get_init_value(QKEYS.CONN_SESS_RTY)
        self.session_retries = create_qlineedit(default=_d, max_len=2)
        _d = self.get_init_value(QKEYS.CONN_SESS_SLP)
        self.session_sleep = create_qlineedit(default=_d, max_len=2)
        _d = self.get_init_value(QKEYS.CONN_API_RTY)
        self.api_retries = create_qlineedit(default=_d, max_len=2)
        _d = self.get_init_value(QKEYS.CONN_API_SLP)
        self.api_sleep = create_qlineedit(default=_d, max_len=2)
        _d = self.get_init_value(QKEYS.CONN_THER_RTY)
        self.ther_boss_retry = create_qlineedit(default=_d, max_len=1)

        self.init_ui()

    def init_ui(self):
        row = 0
        row = self.init_overall(row)
        row = self.init_connections(row)
        row = self.init_thermopylae(row)
        self.init_hack(row)

    def init_overall(self, row: int) -> int:
        self.layout.addWidget(create_qlabel(text='Overall', font_size=HEADER2), row, 0)
        row += 1
        self.layout.addWidget(QHLine(parent=self, color=QColor(0, 0, 0), width=10), row, 0, 1, 5)

        row += 1
        self.layout.addWidget(create_qlabel(text='Random Seed'), row, 0, 1, 1)
        self.seed_input.textChanged.connect(self.set_random_seed)
        self.layout.addWidget(self.seed_input, row, 1, 1, 1)

        row += 1
        speed_label = create_qlabel(text='Game Speed (sec)')
        speed_label.setToolTip("Set server request intervals.\nInvalid inputs will be ignored (such as low > high)")
        self.layout.addWidget(speed_label, row, 0, 1, 1)
        self.layout.addWidget(create_qlabel('Lower Bound'), row, 1, 1, 1)
        _d = self.get_init_value(QKEYS.GAME_SPD_LO)
        self.speed_lo_input.textChanged.connect(lambda res: self.create_input(res, self.speed_lo_input, _d, QKEYS.GAME_SPD_LO))
        self.layout.addWidget(self.speed_lo_input, row, 2, 1, 1)
        self.layout.addWidget(create_qlabel('Upper Bound'), row, 3, 1, 1)
        _d = self.get_init_value(QKEYS.GAME_SPD_HI)
        self.speed_hi_input.textChanged.connect(lambda res: self.create_input(res, self.speed_hi_input, _d, QKEYS.GAME_SPD_HI))
        self.layout.addWidget(self.speed_hi_input, row, 4, 1, 1)
        return row

    def init_connections(self, row: int) -> int:
        row += 1
        self.layout.addWidget(create_qlabel(text='Connection', font_size=HEADER2), row, 0, 1, 1)
        row += 1
        self.layout.addWidget(QHLine(parent=self, color=QColor(0, 0, 0), width=10), row, 0, 1, 5)

        row += 1
        self.layout.addWidget(create_qlabel(text='Retry Limit', font_size=HEADER3), row, 0, 1, 1)
        self.layout.addWidget(create_qlabel(text='session'), row, 1, 1, 1)
        _d = self.get_init_value(QKEYS.CONN_SESS_RTY)
        self.session_retries.textChanged.connect(lambda res: self.create_input(res, self.session_retries, _d, QKEYS.CONN_SESS_RTY))
        self.layout.addWidget(self.session_retries, row, 2, 1, 1)
        self.layout.addWidget(create_qlabel(text='sleep (sec)'), row, 3, 1, 1)
        _d = self.get_init_value(QKEYS.CONN_SESS_SLP)
        self.session_sleep.textChanged.connect(lambda res: self.create_input(res, self.session_sleep, _d, QKEYS.CONN_SESS_SLP))
        self.layout.addWidget(self.session_sleep, row, 4, 1, 1)

        row += 1
        self.layout.addWidget(create_qlabel(text='WGR API'), row, 1, 1, 1)
        _d = self.get_init_value(QKEYS.CONN_API_RTY)
        self.api_retries.textChanged.connect(lambda res: self.create_input(res, self.api_retries, _d, QKEYS.CONN_API_RTY))
        self.layout.addWidget(self.api_retries, row, 2, 1, 1)
        self.layout.addWidget(create_qlabel(text='sleep (sec)'), row, 3, 1, 1)
        _d = self.get_init_value(QKEYS.CONN_API_SLP)
        self.api_sleep.textChanged.connect(lambda res: self.create_input(res, self.api_sleep, _d, QKEYS.CONN_API_SLP))
        self.layout.addWidget(self.api_sleep, row, 4, 1, 1)
        return row

    def init_thermopylae(self, row: int) -> int:
        row += 1
        self.layout.addWidget(create_qlabel(text='Thermopylae'), row, 1, 1, 1)
        _d = self.get_init_value(QKEYS.CONN_THER_RTY)
        self.ther_boss_retry.textChanged.connect(lambda res: self.create_input(res, self.ther_boss_retry, _d, QKEYS.CONN_THER_RTY))
        self.layout.addWidget(self.ther_boss_retry, row, 2, 1, 1)
        row += 1

        return row

    def init_hack(self, row: int) -> None:
        # following is a hack; TODO: setRowStretch is not working properly
        for h in range(10):
            row += 1
            self.layout.addWidget(QLabel(""), row, 0, 1, 4)

    def on_reset(self) -> None:
        _d = self.get_init_value(QKEYS.GAME_RANDOM_SEED, True)
        self.seed_input.setText(str(_d))
        _d = self.get_init_value(QKEYS.GAME_SPD_LO, True)
        self.speed_lo_input.setText(str(_d))
        _d = self.get_init_value(QKEYS.GAME_SPD_HI, True)
        self.speed_hi_input.setText(str(_d))
        _d = self.get_init_value(QKEYS.CONN_SESS_RTY, True)
        self.session_retries.setText(str(_d))
        _d = self.get_init_value(QKEYS.CONN_SESS_SLP, True)
        self.session_sleep.setText(str(_d))
        _d = self.get_init_value(QKEYS.CONN_API_RTY, True)
        self.api_retries.setText(str(_d))
        _d = self.get_init_value(QKEYS.CONN_API_SLP, True)
        self.api_sleep.setText(str(_d))
        _d = self.get_init_value(QKEYS.CONN_THER_RTY, True)
        self.ther_boss_retry.setText(str(_d))

    def create_input(self, _input: str, _edit: QLineEdit, _default: int, _field: str) -> None:
        if _input == '':
            _input = _default
            _edit.setPlaceholderText(str(_default))
        else:
            _input = int(_input)
        self.qsettings.setValue(_field, _input)

    def get_init_value(self, field: str, is_default: bool = False) -> int:
        if (self.qsettings.contains(field) is True) and (is_default is False):
            d = int(self.qsettings.value(field))
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
        if _input == '':
            random.seed(int(time()))
        else:
            random.seed(int(_input))
        self.qsettings.setValue(QKEYS.GAME_RANDOM_SEED, int(_input))


class TabsSettings(QWidget):
    def __init__(self, qsettings):
        super().__init__()
        self.qsettings = qsettings
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        _d = self.get_init_value(QKEYS.THER_BOSS_RTY)
        self.ther_boss1_retry = create_qlineedit(default=_d[0], max_len=1)
        self.ther_boss2_retry = create_qlineedit(default=_d[1], max_len=1)
        self.ther_boss3_retry = create_qlineedit(default=_d[2], max_len=1)
        _d = self.get_init_value(QKEYS.THER_BOSS_STD)
        self.ther_boss1_std = create_qlineedit(default=_d[0], max_len=1)
        self.ther_boss2_std = create_qlineedit(default=_d[1], max_len=1)
        self.ther_boss3_std = create_qlineedit(default=_d[2], max_len=1)

        self.init_ui()

    def init_ui(self):
        row = 0
        row = self.init_thermopylae(row)
        self.init_hack(row)

    def init_thermopylae(self, row: int) -> int:
        self.layout.addWidget(create_qlabel(text='Thermopylae', font_size=HEADER3), row, 0)
        self.layout.addWidget(create_qlabel(text='Bosses Retries'), row, 1)
        _d = self.get_init_value(QKEYS.THER_BOSS_RTY)
        self.ther_boss1_retry.textChanged.connect(lambda res: self.create_input(res, self.ther_boss1_retry, _d, 0, QKEYS.THER_BOSS_RTY))
        self.layout.addWidget(self.ther_boss1_retry, row, 2)
        self.ther_boss2_retry.textChanged.connect(lambda res: self.create_input(res, self.ther_boss2_retry, _d, 1, QKEYS.THER_BOSS_RTY))
        self.layout.addWidget(self.ther_boss2_retry, row, 3)
        self.ther_boss3_retry.textChanged.connect(lambda res: self.create_input(res, self.ther_boss3_retry, _d, 2, QKEYS.THER_BOSS_RTY))
        self.layout.addWidget(self.ther_boss3_retry, row, 4)

        row += 1
        ther_boss_retry_std_label = create_qlabel(text='On sunken')
        ther_boss_retry_std_label.setToolTip("Sunken at least how many enemies to disable boss re-fight")
        self.layout.addWidget(ther_boss_retry_std_label, row, 1)
        _d = self.get_init_value(QKEYS.THER_BOSS_STD)
        self.ther_boss1_std.textChanged.connect(lambda res: self.create_input(res, self.ther_boss1_std, _d, 0, QKEYS.THER_BOSS_STD))
        self.layout.addWidget(self.ther_boss1_std, row, 2)
        self.ther_boss2_std.textChanged.connect(lambda res: self.create_input(res, self.ther_boss2_std, _d, 1, QKEYS.THER_BOSS_STD))
        self.layout.addWidget(self.ther_boss2_std, row, 3)
        self.ther_boss3_std.textChanged.connect(lambda res: self.create_input(res, self.ther_boss3_std, _d, 2, QKEYS.THER_BOSS_STD))
        self.layout.addWidget(self.ther_boss3_std, row, 4)

        row += 1
        return row

    def init_hack(self, row: int) -> None:
        # following is a hack; TODO: setRowStretch is not working properly
        for h in range(10):
            row += 1
            self.layout.addWidget(QLabel(""), row, 0, 1, 4)

    def create_input(self, _input: str, _edit: QLineEdit, _default: list, idx: int, _field: str) -> None:
        if _input == '':
            save = _default
            _edit.setPlaceholderText(str(_default[idx]))
        else:
            x = int(_input)
            if _field == QKEYS.THER_BOSS_STD:
                if (x < 0) or (x > 6):
                    x = 2
            _default[idx] = x
            save = _default
        self.qsettings.setValue(_field, save)

    def on_reset(self) -> None:
        _d = self.get_init_value(QKEYS.THER_BOSS_RTY, True)
        self.ther_boss1_retry.setText(str(_d[0]))
        self.ther_boss1_retry.setText(str(_d[1]))
        self.ther_boss1_retry.setText(str(_d[2]))

        _d = self.get_init_value(QKEYS.THER_BOSS_STD, True)
        self.ther_boss1_std.setText(str(_d[0]))
        self.ther_boss2_std.setText(str(_d[1]))
        self.ther_boss3_std.setText(str(_d[2]))

    def get_init_value(self, field: str, is_default: bool = False) -> list:
        if (self.qsettings.contains(field) is True) and (is_default is False):
            d = self.qsettings.value(field)
        else:
            if field == QKEYS.THER_BOSS_RTY:
                d = [3, 5, 10]
            elif field == QKEYS.THER_BOSS_STD:
                d = [1, 2, 2]
            else:
                logging.error(f"Unsupported QKEYS filed {field}")
        return d

# End of File
