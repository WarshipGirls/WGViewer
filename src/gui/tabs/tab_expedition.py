import os
import sys
from collections import Callable

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QButtonGroup

from src.func import logger_names as QLOGS
from src.func.log_handler import get_new_logger
from src.gui.side_dock.dock import SideDock
from .expedition.table import ExpTable
from .expedition.summary import DailySummary
from .expedition.fleets import ExpFleets
from .expedition.ui_widgets import PopupFleets


# TODO: get real-time data

def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabExpedition(QWidget):
    def __init__(self, tab_name: str, side_dock: SideDock):
        super().__init__()
        self.setObjectName(tab_name)
        self.side_dock = side_dock

        # Lesson: to append to the textedit, logger must be passed down to child widget; using same name doesn't help
        self.right_text_box = QTextEdit()
        self.logger = get_new_logger(name=QLOGS.TAB_EXP, level=QLOGS.LVL_INFO, signal=self.right_text_box.append)

        self.button_table = QPushButton("Open &Expedition Table")
        self.set_exp_buttons = QButtonGroup()
        self._popup = None
        csv_path = get_data_path('assets/data/exp_data.csv')
        self.table = ExpTable(self, csv_path)
        self.summary = DailySummary(self.logger)
        self.fleet_table = ExpFleets(self.side_dock, self.summary, self.logger)

        self.init_ui()

    def select_expedition_fleet(self, fleet_id: str):
        # TODO delete later
        self._popup = PopupFleets(fleet_id)

    def add_button(self, text: str, func: Callable, fleet_id: str) -> QPushButton:
        w = QWidget()
        b = QPushButton()
        b.setText(text)
        b.clicked.connect(lambda: func(fleet_id))
        self.set_exp_buttons.addButton(b)
        return b

    def init_ui(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        right_layout = QVBoxLayout()
        self.right_text_box.setFont(QFont('Consolas'))
        self.right_text_box.setFontPointSize(10)
        self.right_text_box.setReadOnly(True)

        bottom_right_layout = QHBoxLayout()
        bottom_right_layout.addWidget(self.summary)
        bottom_right_buttons_layout = QVBoxLayout()
        self.button_table.clicked.connect(self.on_button_table_clicked)
        bottom_right_buttons_layout.addWidget(self.button_table)
        for i in range(5, 9):
            t = f'Set Expedition Fleet #{i}'
            b = self.add_button(t, self.select_expedition_fleet, str(i))
            bottom_right_buttons_layout.addWidget(b)

        bottom_right_layout.addLayout(bottom_right_buttons_layout)
        bottom_right_layout.setStretch(0, 0)
        bottom_right_layout.setStretch(1, 1)

        right_layout.addWidget(self.right_text_box)
        right_layout.addLayout(bottom_right_layout)
        right_layout.setStretch(0, 1)
        right_layout.setStretch(1, 0)
        main_layout.addWidget(self.fleet_table)
        main_layout.addLayout(right_layout)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        self.setLayout(main_layout)

    def on_button_table_clicked(self) -> None:
        self.table.show()

    @pyqtSlot()
    def on_table_close(self):
        self.table.hide()

# End of File
