import logging
from time import sleep

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QButtonGroup

import src.data as wgv_data
from src.func.worker import Worker

from src.wgr.six import API_SIX
from src.func.log_handler import LogHandler
from src.gui.side_dock.resource_model import ResourceTableModel
from src.gui.side_dock.dock import SideDock
from .thermopylae.ship_window import ShipSelectWindow
from .thermopylae.sortie import Sortie


class TabThermopylae(QWidget):
    sig_fuel = pyqtSignal(int)
    sig_ammo = pyqtSignal(int)
    sig_steel = pyqtSignal(int)
    sig_baux = pyqtSignal(int)
    sig_exp = pyqtSignal(dict)

    def __init__(self, tab_name: str, side_dock: SideDock, is_realrun: bool):
        # TODO reorganize
        super().__init__()
        self.setObjectName(tab_name)
        self.side_dock = side_dock
        self.resource_info: ResourceTableModel = self.side_dock.table_model
        self.is_realrun = is_realrun

        self.sig_fuel.connect(self.resource_info.update_fuel)
        self.sig_ammo.connect(self.resource_info.update_ammo)
        self.sig_steel.connect(self.resource_info.update_steel)
        self.sig_baux.connect(self.resource_info.update_bauxite)
        self.sig_exp.connect(self.side_dock.update_lvl_label)

        self.api_six = API_SIX(wgv_data.load_cookies())
        self.fleets = [None] * 6
        self.final_fleet = [None] * 14
        # for testing
        self.final_fleet = []

        self.main_layout = QHBoxLayout(self)
        # TODO separate bar info
        self.button_container = QWidget()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.ticket_label = None
        self.purchasable_label = None
        self.set_info_bar()

        self.button_group = None
        self.button_pre_battle = None
        self.button_fresh_sortie = None
        self.button_resume_sortie = None
        self.init_left_layout()

        self.right_text_box = QTextEdit()
        self.init_right_layout()

        self.logger = self.get_logger()

        self.w = None
        self.init_ui()
        self.sortie = Sortie(self, self.api_six, [], [], self.is_realrun)

        self.bee_pre_battle = Worker(self.sortie.pre_battle, ())
        self.bee_pre_battle.finished.connect(self.pre_battle_finished)
        self.bee_pre_battle.terminate()
        self.bee_fresh_sortie = None
        self.bee_resume_sortie = None

    def get_logger(self) -> logging.Logger:
        logger = logging.getLogger('TabThermopylae')
        log_handler = LogHandler()
        log_handler.sig_log.connect(self.right_text_box.append)
        logger.addHandler(log_handler)
        log_handler.setLevel(level=logging.INFO)
        return logger

    def set_info_bar(self) -> None:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        ticket_tag = QLabel("Remaining Sortie Tickets")
        self.ticket_label = QLabel("?")
        can_buy_tag = QLabel("Purchasable Tickets")
        self.purchasable_label = QLabel("?")
        layout.addWidget(ticket_tag)
        layout.addWidget(self.ticket_label)
        layout.addWidget(can_buy_tag)
        layout.addWidget(self.purchasable_label)
        w.setLayout(layout)
        for i in range(4):
            layout.setStretch(i, 0)
        self.left_layout.addWidget(w)

    def update_ticket(self, data: int) -> None:
        self.ticket_label.setText(str(data))

    def update_purchasable(self, data: int) -> None:
        self.purchasable_label.setText(str(data))

    def init_ui(self) -> None:
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 1)
        self.setLayout(self.main_layout)

        # self.add_ship()

    def init_left_layout(self) -> None:
        t = QTextEdit()
        msg = "Notes\n"
        msg += "1. As of now, this auto sortie function is ONLY for players who passed E6 manually;\n"
        msg += "2. As of now, there are limitations on what ship should be set:\n"
        msg += "    - DD 'Glowworm' and 'Amethyst', and CV 'Indomitable' are required\n"
        msg += "    - 6 high level SS are required\n"
        msg += "3. Adjutant 紫貂 (default) and Habakkuk (purchased in shop) are required;\n"
        msg += "4. The function is NOT completed yet.\n"
        t.setFontPointSize(10)
        t.setText(msg)

        self.button_pre_battle = QPushButton('Perform pre-battle checking')
        self.button_pre_battle.clicked.connect(self.on_pre_battle)
        self.button_pre_battle.setEnabled(True)

        self.button_fresh_sortie = QPushButton('Start a new E6 combat')
        self.button_fresh_sortie.clicked.connect(self.on_fresh_sortie)
        self.button_fresh_sortie.setEnabled(False)

        self.button_resume_sortie = QPushButton('Resume E6 combat')
        self.button_resume_sortie.clicked.connect(self.on_resume_sortie)
        self.button_resume_sortie.setEnabled(False)

        self.left_layout.addWidget(t)
        self.left_layout.addWidget(self.button_pre_battle)
        self.left_layout.addWidget(self.button_fresh_sortie)
        self.left_layout.addWidget(self.button_resume_sortie)

    def init_right_layout(self) -> None:
        self.right_text_box.setFont(QFont('Consolas'))
        self.right_text_box.setFontPointSize(10)
        self.right_text_box.setReadOnly(True)
        self.right_layout.addWidget(self.right_text_box)

    def add_ship(self) -> None:
        # TODO long term; not used right now; let user select boats here; now just use last fleets
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

    def disable_sortie(self) -> None:
        raise NotImplementedError

    def handle_selection(self, ship_info: list, button_id: int) -> None:
        b = self.button_group.buttons()[button_id]
        ship_id = ship_info[1]
        if int(ship_id) in self.fleets:
            b.setText('! SHIP ALREADY EXISTS IN FLEET !')
        else:
            self.fleets[button_id] = int(ship_id)
            s = ", ".join(ship_info)
            b.setText(s)

    def popup_select_window(self, btn_id: int) -> None:
        # TODO: delete obj after close
        self.w = ShipSelectWindow(self, btn_id)
        self.w.show()

    # ================================
    # On thread start
    # ================================

    def on_pre_battle(self) -> None:
        self.button_pre_battle.setEnabled(True)
        self.bee_pre_battle.start()

    def on_fresh_sortie(self) -> None:
        self.button_fresh_sortie.setEnabled(False)
        self.button_resume_sortie.setEnabled(False)
        self.bee_fresh_sortie.start()

    def on_resume_sortie(self) -> None:
        self.button_fresh_sortie.setEnabled(False)
        self.button_resume_sortie.setEnabled(False)
        self.bee_resume_sortie.start()

    # ================================
    # On thread finished
    # ================================

    def sortie_finished(self) -> None:
        self.logger.info('==== Sortie (dev) is done! ====')
        self.button_fresh_sortie.setEnabled(True)
        self.button_resume_sortie.setEnabled(True)

    def pre_battle_finished(self) -> None:
        self.logger.info('==== Pre battle checking is done! ====')
        self.bee_fresh_sortie = Worker(self.sortie.start_fresh_sortie, ())
        self.bee_fresh_sortie.finished.connect(self.sortie_finished)
        self.bee_fresh_sortie.terminate()
        self.bee_resume_sortie = Worker(self.sortie.resume_sortie, ())
        self.bee_resume_sortie.finished.connect(self.sortie_finished)
        self.bee_resume_sortie.terminate()

    # ================================
    # Update Side Dock
    # ================================

    def update_resources(self, f: int, a: int, s: int, b: int) -> None:
        # signals has to be emitted from a QObject
        self.sig_fuel.emit(f)
        self.sig_ammo.emit(a)
        self.sig_steel.emit(s)
        self.sig_baux.emit(b)

    def update_user_exp_label(self, x: dict) -> None:
        self.sig_exp.emit(x)

# End of File
