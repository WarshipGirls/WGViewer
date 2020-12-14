import logging
import random

from time import time

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QFont, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton

from src.gui.custom_widgets import QHLine

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
        self.handle_tab_init(self.tab_adv, 'UI/TAB/advance')
        self.tab_exp = QCheckBox("Expedition", self)
        self.handle_tab_init(self.tab_exp, 'UI/TAB/expedition')
        self.tab_ship = QCheckBox("Dock", self)
        self.handle_tab_init(self.tab_ship, 'UI/TAB/ship')
        self.tab_ther = QCheckBox("Thermopylae", self)
        self.handle_tab_init(self.tab_ther, 'UI/TAB/thermopylae')

        self.init_page_ui()

    def init_page_ui(self) -> None:
        row = 0
        header = create_qlabel(text="ON START", font_size=HEADER2)
        self.layout.addWidget(header, row, 0, 1, 4)

        row += 1
        h2 = create_qlabel(text="SIDE DOCK", font_size=HEADER3)
        self.layout.addWidget(h2, row, 0, 1, 4)
        row += 1
        self.layout.addWidget(QHLine(parent=self, color=QColor(0, 0, 0), width=10), row, 0, 1, 4)
        row += 1
        if self.qsettings.value('UI/no_side_dock') == 'true':
            self.side_dock.setChecked(False)
        else:
            self.side_dock.setChecked(True)
        self.layout.addWidget(self.side_dock, row, 0, 1, 1)
        self.dropdown_side_dock.setToolTip("Set the default position of side dock")
        self.dropdown_side_dock.addItems(['Right', 'Left'])
        self.layout.addWidget(self.dropdown_side_dock, row, 1, 1, 1)

        row += 1
        h3 = create_qlabel(text="TABS", font_size=12)
        self.layout.addWidget(h3, row, 0, 1, 4)
        row += 1
        self.layout.addWidget(QHLine(parent=self, color=QColor(0, 0, 0), width=10), row, 0, 1, 4)
        row += 1
        if self.qsettings.value('UI/TABS/advance') == 'true':
            self.tab_adv.setChecked(True)
        else:
            self.tab_adv.setChecked(False)

        if self.qsettings.value('UI/TABS/expedition') == 'true':
            self.tab_exp.setChecked(True)
        else:
            self.tab_exp.setChecked(False)

        if self.qsettings.value('UI/TABS/ship') == 'true':
            self.tab_ship.setChecked(True)
        else:
            self.tab_ship.setChecked(False)

        if self.qsettings.value('UI/TABS/thermopylae') == 'true':
            self.tab_ther.setChecked(True)
        else:
            self.tab_ther.setChecked(False)
        self.layout.addWidget(self.tab_adv, row, 0, 1, 1)
        self.layout.addWidget(self.tab_exp, row, 1, 1, 1)
        self.layout.addWidget(self.tab_ship, row, 2, 1, 1)
        self.layout.addWidget(self.tab_ther, row, 3, 1, 1)

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
            self.qsettings.setValue('UI/side_dock_pos', 'right')
        elif self.dropdown_side_dock.currentText() == 'Left':
            self.qsettings.setValue(('UI/side_dock_pos', 'left'))
        else:
            self.qsettings.setValue('UI/side_dock_pos', 'right')

    def handle_side_dock_init(self) -> None:
        if self.side_dock.isChecked() is True:
            self.qsettings.setValue('UI/no_side_dock', False)
        else:
            self.qsettings.setValue('UI/no_side_dock', True)

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

        _d = self.get_init_value('GAME/random_seed')
        self.seed_input = self.create_qlineedit(default=_d, max_len=16)
        _d = self.get_init_value('GAME/speed_lo_bound')
        self.speed_lo_input = self.create_qlineedit(default=_d, max_len=3)
        _d = self.get_init_value('GAME/speed_hi_bound')
        self.speed_hi_input = self.create_qlineedit(default=_d, max_len=3)
        _d = self.get_init_value('CONNECTION/session_retries')
        self.session_retries = self.create_qlineedit(default=_d, max_len=2)
        _d = self.get_init_value('CONNECTION/session_sleep')
        self.session_sleep = self.create_qlineedit(default=_d, max_len=2)
        _d = self.get_init_value('CONNECTION/api_retries')
        self.api_retries = self.create_qlineedit(default=_d, max_len=2)
        _d = self.get_init_value('CONNECTION/api_sleep')
        self.api_sleep = self.create_qlineedit(default=_d, max_len=2)

        self.init_ui()

    @staticmethod
    def create_qlineedit(default: int, max_len: int) -> QLineEdit:
        q = QLineEdit()
        q.setPlaceholderText(str(default))
        q.setMaxLength(max_len)
        q.setValidator(get_int_mask())
        return q

    def init_ui(self):
        row = 0
        self.layout.addWidget(create_qlabel(text='Overall', font_size=HEADER2))
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
        _d = self.get_init_value('GAME/speed_lo_bound')
        self.speed_lo_input.textChanged.connect(lambda res: self.create_input(res, self.speed_lo_input, _d, 'GAME/speed_lo_bound'))
        self.layout.addWidget(self.speed_lo_input, row, 2, 1, 1)
        self.layout.addWidget(create_qlabel('Upper Bound'), row, 3, 1, 1)
        _d = self.get_init_value('GAME/speed_hi_bound')
        self.speed_hi_input.textChanged.connect(lambda res: self.create_input(res, self.speed_hi_input, _d, 'GAME/speed_hi_bound'))
        self.layout.addWidget(self.speed_hi_input, row, 4, 1, 1)

        row += 1
        self.layout.addWidget(create_qlabel(text='Connection', font_size=HEADER2), row, 0, 1, 1)
        row += 1
        self.layout.addWidget(QHLine(parent=self, color=QColor(0, 0, 0), width=10), row, 0, 1, 5)

        row += 1
        self.layout.addWidget(create_qlabel(text='Retry Limit', font_size=HEADER3), row, 0, 1, 1)
        self.layout.addWidget(create_qlabel(text='session'), row, 1, 1, 1)
        _d = self.get_init_value('CONNECTION/session_retries')
        self.session_retries.textChanged.connect(lambda res: self.create_input(res, self.session_retries, _d, 'CONNECTION/session_retries'))
        self.layout.addWidget(self.session_retries, row, 2, 1, 1)
        self.layout.addWidget(create_qlabel(text='sleep (sec)'), row, 3, 1, 1)
        _d = self.get_init_value('CONNECTION/session_sleep')
        self.session_sleep.textChanged.connect(lambda res: self.create_input(res, self.session_sleep, _d, 'CONNECTION/session_sleep'))
        self.layout.addWidget(self.session_sleep, row, 4, 1, 1)

        row += 1
        self.layout.addWidget(create_qlabel(text='WGR API'), row, 1, 1, 1)
        _d = self.get_init_value('CONNECTION/api_retries')
        self.api_retries.textChanged.connect(lambda res: self.create_input(res, self.api_retries, _d, 'CONNECTION/api_retries'))
        self.layout.addWidget(self.api_retries, row, 2, 1, 1)
        self.layout.addWidget(create_qlabel(text='sleep (sec)'), row, 3, 1, 1)
        _d = self.get_init_value('CONNECTION/api_sleep')
        self.api_sleep.textChanged.connect(lambda res: self.create_input(res, self.api_sleep, _d, 'CONNECTION/api_sleep'))
        self.layout.addWidget(self.api_sleep, row, 4, 1, 1)

        # following is a hack; TODO: setRowStretch is not working properly
        for h in range(10):
            row += 1
            self.layout.addWidget(QLabel(""), row, 0, 1, 4)

    def on_reset(self) -> None:
        _d = self.get_init_value('GAME/random_seed', True)
        self.seed_input.setText(str(_d))
        # self.seed_input.setPlaceholderText(str(_d))
        _d = self.get_init_value('GAME/speed_lo_bound', True)
        self.speed_lo_input.setText(str(_d))
        # self.speed_lo_input.setPlaceholderText(str(_d))
        _d = self.get_init_value('GAME/speed_hi_bound', True)
        self.speed_hi_input.setText(str(_d))
        # self.speed_hi_input.setPlaceholderText(str(_d))
        _d = self.get_init_value('CONNECTION/session_retries', True)
        # self.session_retries.setPlaceholderText(str(_d))
        self.session_retries.setText(str(_d))
        _d = self.get_init_value('CONNECTION/session_sleep', True)
        self.session_sleep.setText(str(_d))
        # self.session_sleep.setPlaceholderText(str(_d))
        _d = self.get_init_value('CONNECTION/api_retries', True)
        self.api_retries.setText(str(_d))
        # self.api_retries.setPlaceholderText(str(_d))
        _d = self.get_init_value('CONNECTION/api_sleep', True)
        self.api_sleep.setText(str(_d))
        # self.api_sleep.setPlaceholderText(str(_d))

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
            if field == 'GAME/random_seed':
                d = 42
            elif field == 'GAME/speed_lo_bound':
                d = 5
            elif field == 'GAME/speed_hi_bound':
                d = 10
            elif field == 'CONNECTION/session_retries':
                d = 5
            elif field == 'CONNECTION/session_sleep':
                d = 3
            elif field == 'CONNECTION/api_retries':
                d = 5
            elif field == 'CONNECTION/api_sleep':
                d = 3
            else:
                d = 10
                logging.error(field)
        return d

    def set_random_seed(self, _input: str) -> None:
        if _input == '':
            random.seed(int(time()))
        else:
            random.seed(int(_input))
        self.qsettings.setValue('GAME/random_seed', int(_input))

# End of File
