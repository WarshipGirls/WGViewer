import logging
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QTableWidget, QMainWindow, QTableWidgetItem, QButtonGroup

import src.data as wgr_data
from src.func.worker import Worker

from src.wgr.six import API_SIX
from src.func.log_handler import LogHandler
from .thermopylae.ship_window import ShipSelectWindow
from .thermopylae.sortie import Sortie


class TabThermopylae(QWidget):
    def __init__(self, tab_name: str):
        super().__init__()
        self.setObjectName(tab_name)
        self.api_six = API_SIX(wgr_data.load_cookies())
        self.fleets = [None] * 6
        self.final_fleet = [None] * 14
        # for testing
        self.final_fleet = []

        self.main_layout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.button_group = None
        self.button1 = None
        self.sortie_button = None
        self.init_left_layout()

        text_box = QTextEdit()
        text_box.setReadOnly(True)
        self.right_layout.addWidget(text_box)
        self.bee = Worker(self.test_process, ())
        self.bee.finished.connect(self.process_finished)
        self.bee.terminate()

        self.logger = logging.getLogger('TabThermopylae')
        log_handler = LogHandler()
        log_handler.sig_log.connect(text_box.append)
        self.logger.addHandler(log_handler)

        self.init_ui()

    def init_ui(self) -> None:
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 1)
        self.setLayout(self.main_layout)

        self.add_ship()

    def init_left_layout(self) -> None:
        self.button1 = QPushButton('start random process')
        self.sortie_button = QPushButton('Start Thermopylae E6 sortieing...')
        self.button1.clicked.connect(self.button1_on_click)
        self.sortie_button.clicked.connect(self.on_sortie)

        self.left_layout.addWidget(self.button1)
        self.left_layout.addWidget(self.sortie_button)

    def add_ship(self):
        self.button_group = QButtonGroup()
        # for ship_id in self.fleets:
        for i in range(len(self.fleets)):
            t = self.fleets[i]
            l = QPushButton()
            if t is None:
                l.setText('+')
            else:
                l.setText(str(t))
            l.clicked.connect(lambda _, _i=i: self.popup_select_window(_i))
            self.button_group.addButton(l)
            self.left_layout.addWidget(l)

    def handle_selection(self, ship_info: list, button_id: int):
        b = self.button_group.buttons()[button_id]
        ship_id = ship_info[1]
        if int(ship_id) in self.fleets:
            b.setText('! SHIP ALREADY EXISTS IN FLEET !')
        else:
            self.fleets[button_id] = int(ship_id)
            s = ", ".join(ship_info)
            b.setText(s)

    def popup_select_window(self, btn_id):
        # TODO: delete obj after close
        self.w = ShipSelectWindow(self, btn_id)
        self.w.show()

    def button1_on_click(self):
        self.button1.setEnabled(False)
        self.bee.start()

    def test_process(self):
        # button 1 linked
        self.logger.info('starting')
        for i in range(10):
            self.logger.info(i)
            sleep(1)

    def on_sortie(self):
        self.logger.info('User clicked sortieing button...')
        # TODO TODO TEST
        Sortie(self.api_six, [], [], self.logger)

    def process_finished(self):
        self.logger.info('task is done')
        self.button1.setEnabled(True)

# End of File
