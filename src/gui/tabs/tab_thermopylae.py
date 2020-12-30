from PyQt5.QtCore import pyqtSignal, QTimer, QSettings
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy,
    QWidget, QLabel, QTextEdit, QPushButton, QButtonGroup, QSpinBox
)

from src import data as wgv_data
from src.utils import stop_sleep_event, reset_sleep_event
from src.func.worker import CallbackWorker
from src.func import logger_names as QLOGS
from src.func import qsettings_keys as QKEYS
from src.func.log_handler import get_new_logger
from src.gui.custom_widgets import ClickableLabel
from src.gui.side_dock.resource_model import ResourceTableModel
from src.gui.side_dock.dock import SideDock
from src.utils import set_sleep
from src.wgr import API_SIX
from .thermopylae.ship_window import ShipSelectWindow
from .thermopylae.sortie import Sortie


class TabThermopylae(QWidget):
    """
    Thermopylae, JueZhan Mode, first introduced in Game v5.0.0 (CN server).
    This tab is meant for automatically farming Thermopylae Ex-6 (the last chapter of the mode),
        which was the primary reason that brings WGViewer into real world.
    """
    sig_fuel = pyqtSignal(int)
    sig_ammo = pyqtSignal(int)
    sig_steel = pyqtSignal(int)
    sig_baux = pyqtSignal(int)
    sig_repair = pyqtSignal(int)
    sig_exp = pyqtSignal(dict)

    def __init__(self, tab_name: str, side_dock: SideDock, is_realrun: bool):
        super().__init__()
        self.setObjectName(tab_name)
        self.side_dock = side_dock
        self.resource_info: ResourceTableModel = self.side_dock.table_model
        self.is_realrun = is_realrun

        # Signals
        self.sig_fuel.connect(self.resource_info.update_fuel)
        self.sig_ammo.connect(self.resource_info.update_ammo)
        self.sig_steel.connect(self.resource_info.update_steel)
        self.sig_baux.connect(self.resource_info.update_bauxite)
        self.sig_repair.connect(self.resource_info.update_repair)
        self.sig_exp.connect(self.side_dock.update_lvl_label)

        # Members
        self.api = API_SIX(wgv_data.load_cookies())
        self.qsettings = QSettings(wgv_data.get_qsettings_file(), QSettings.IniFormat)
        self.user_ships = wgv_data.get_processed_userShipVo()
        self.battle_fleet: list = [None] * 6
        self.escort_DD: list = [None] * 2
        self.escort_CV: list = [None]
        self.user_chosen_cid: list = [None] * 9
        self.ship_select_window = None

        self.sortie = None
        # Threads
        self.bee_pre_battle = None
        self.bee_fresh_sortie = None
        self.bee_resume_sortie = None

        # UI members
        self.main_layout = QHBoxLayout(self)
        self.left_layout = QGridLayout()
        self.right_layout = QVBoxLayout()

        self.ticket_label = QLabel("?")
        self.button_purchase = QPushButton("?")
        self.adjutant_label = QLabel("?")
        self.adjutant_exp_label = QLabel("?/?")
        self.points_label = QLabel("?")

        self._label = None
        self._is_first_timer: bool = True
        self._is_speed_mode: bool = False
        self._clicks: int = 0
        self._is_timer_start: bool = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._check_label)

        self.set_ticket_display()
        self.set_adjutant_display()

        self.ship_button_group = QButtonGroup()
        self.boat_pool_label = QLabel()
        self.fleet_label = QLabel()
        self.ui_buttons = QButtonGroup()
        self.button_set_ships = QPushButton('&Set fleet')
        self.button_pre_battle = QPushButton('&Pre-Battle Check')
        self.button_fresh_sortie = QPushButton('Fresh &Combat')
        self.button_resume_sortie = QPushButton('&Resume Combat')
        self.button_stop_sortie = QPushButton('Stop Task')
        self.multi_runs = QSpinBox()
        self.init_left_layout()

        self.right_text_box = QTextEdit()
        # after right_text_box creation
        self.logger = get_new_logger(name=QLOGS.TAB_THER, level=QLOGS.LVL_INFO, signal=self.right_text_box.append)
        self.init_right_layout()
        self.init_ui()

    def init_ui(self) -> None:
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 1)
        self.setLayout(self.main_layout)

    def init_left_layout(self) -> None:
        self.button_purchase.setEnabled(False)
        t = QTextEdit()
        msg = "Notes\n"
        msg += "1. As of now, this auto sortie function is ONLY for players who passed E6 manually;\n"
        msg += "2. Adjutant 紫貂 (default) and Habakkuk (purchased in shop) are required;\n"
        msg += "3. Ships under Lv. 80 cannot be selected.\n"
        msg += "\nHow to Use\n"
        msg += "1. Select ships (rest non-battle ships are selected from old settings), then press 'Set fleet'\n"
        msg += "2. Press 'Pre-Battle Check'\n"
        msg += "3. Adjust your desired sortie times\n"
        msg += "4. Press 'Fresh Combat' or 'Resume Combat'\n"
        msg += "?. Now just wait or find an easter egg to boost sortie speed"
        t.setFontPointSize(10)
        t.setText(msg)
        t.setReadOnly(True)

        self.boat_pool_label.setFont(QFont('Consolas'))
        self.boat_pool_label.setWordWrap(True)
        self.boat_pool_label.setText('BOAT POOL |')
        self.fleet_label.setFont(QFont('Consolas'))
        self.fleet_label.setWordWrap(True)
        self.fleet_label.setText('ON BATTLE |')

        self.button_set_ships.clicked.connect(self.check_selections)
        self.ui_buttons.addButton(self.button_set_ships)

        self.button_pre_battle.clicked.connect(self.on_pre_battle)
        self.ui_buttons.addButton(self.button_pre_battle)

        self.button_fresh_sortie.clicked.connect(self.on_fresh_sortie)
        self.ui_buttons.addButton(self.button_fresh_sortie)

        self.button_resume_sortie.clicked.connect(self.on_resume_sortie)
        self.ui_buttons.addButton(self.button_resume_sortie)

        self.multi_runs.setEnabled(False)
        self.multi_runs.setSuffix(" times")

        self.button_stop_sortie.clicked.connect(self.disable_sortie)
        self.ui_buttons.addButton(self.button_stop_sortie)

        for b in self.ui_buttons.buttons():
            b.setEnabled(False)
        self.button_set_ships.setEnabled(True)

        self.left_layout.addWidget(t, 3, 0, 1, 4)
        if self.qsettings.contains(QKEYS.THER_DD) and self.qsettings.contains(QKEYS.THER_CV) and self.qsettings.contains(QKEYS.THER_SS):
            self.escort_DD: list = list(map(int, self.qsettings.value(QKEYS.THER_DD)))
            self.escort_CV: list = list(map(int, self.qsettings.value(QKEYS.THER_CV)))
            self.battle_fleet: list = list(map(int, self.qsettings.value(QKEYS.THER_SS)))
            ssb = self.set_ship_selection_buttons(dd=self.escort_DD, cv=self.escort_CV, ss=self.battle_fleet)
        else:
            ssb = self.set_ship_selection_buttons()
        self.left_layout.addWidget(ssb, 4, 0, 2, 4)
        self.left_layout.addWidget(self.button_set_ships, 6, 0, 1, 2)
        self.left_layout.addWidget(self.button_pre_battle, 6, 2, 1, 2)

        self.left_layout.addWidget(self.fleet_label, 7, 0, 1, 4)
        self.left_layout.addWidget(self.boat_pool_label, 8, 0, 1, 4)
        self.left_layout.addWidget(self.button_fresh_sortie, 9, 0)
        self.left_layout.addWidget(self.button_resume_sortie, 9, 1)
        self.left_layout.addWidget(self.multi_runs, 9, 2)
        self.left_layout.addWidget(self.button_stop_sortie, 9, 3)

        self.left_layout.setRowStretch(3, 5)
        self.left_layout.setRowStretch(4, 1)

    def init_right_layout(self) -> None:
        self.right_text_box.setFont(QFont('Consolas'))
        self.right_text_box.setFontPointSize(10)
        self.right_text_box.setReadOnly(True)
        self.right_layout.addWidget(self.right_text_box)

    def set_ticket_display(self) -> None:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button_purchase.clicked.connect(self.on_purchase_clicked)
        layout.addWidget(QLabel("Remaining Sortie Tickets"))
        layout.addWidget(self.ticket_label)
        layout.addWidget(QLabel("Purchasable Tickets"))
        layout.addWidget(self.button_purchase)
        w.setLayout(layout)
        for i in range(4):
            layout.setStretch(i, 0)
        self.left_layout.addWidget(w, 0, 0, 1, 4)

    def set_adjutant_display(self) -> None:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel("Adjutant"))
        layout.addWidget(self.adjutant_label)
        layout.addWidget(self.adjutant_exp_label)

        # secret switch for disable sleep event
        self._label = ClickableLabel()
        self._label.setText("Point")
        self._label.clicked.connect(self._label_clicked)
        layout.addWidget(self._label)

        layout.addWidget(self.points_label)
        w.setLayout(layout)
        self.left_layout.addWidget(w, 1, 0, 1, 4)

    def disable_sortie_widgets(self):
        for b in self.ship_button_group.buttons():
            b.setEnabled(False)
        for b in self.ui_buttons.buttons():
            b.setEnabled(False)
        self.multi_runs.setEnabled(False)

    def enable_sortie_widgets(self):
        for b in self.ship_button_group.buttons():
            b.setEnabled(True)
        for b in self.ui_buttons.buttons():
            b.setEnabled(True)
        self.multi_runs.setEnabled(True)

    # ================================
    # Signals
    # ================================

    def _label_clicked(self) -> None:
        if self._is_speed_mode:
            return
        if self._is_timer_start:
            self._clicks += 1
        else:
            if self._is_first_timer:
                self._timer.start(2000)
                self._is_timer_start = True
                self._is_first_timer = False
            else:
                pass

    def _check_label(self) -> None:
        self._timer.stop()
        if self._clicks > 10:
            self._is_speed_mode = True
            self.logger.warning("WGViewer boost is ON!")
            stop_sleep_event()
        else:
            self._is_speed_mode = False
            self._is_timer_start = False
            self._is_first_timer = True
        self._clicks = 0

    def disable_sortie(self) -> None:
        stop_sleep_event()
        self.button_stop_sortie.setEnabled(False)
        if self.bee_fresh_sortie.isRunning():
            self.logger.debug('fresh-sortie thread is running...')
            self.sortie.stop()
        elif self.bee_resume_sortie.isRunning():
            self.logger.debug('resume-sortie thread is running...')
            self.sortie.stop()
        # elif self.bee_pre_battle.isRunning():
        #     self.logger.debug('pre-battle checking thread is running...')
        #     self.sortie.stop()
        else:
            self.logger.debug('No thread to disable')

    def on_purchase_clicked(self) -> None:
        self.sortie.buy_ticket()

    def on_pre_battle(self) -> None:
        self.disable_sortie_widgets()
        self.qsettings.setValue(QKEYS.THER_DD, self.escort_DD)
        self.qsettings.setValue(QKEYS.THER_CV, self.escort_CV)
        self.qsettings.setValue(QKEYS.THER_SS, self.battle_fleet)

        self.sortie = Sortie(self, self.api, self.escort_DD, self.escort_CV, self.battle_fleet, self.is_realrun)

        self.bee_pre_battle = CallbackWorker(self.sortie.pre_battle, (), self.pre_battle_finished)
        self.bee_pre_battle.terminate()
        self.bee_fresh_sortie = CallbackWorker(self.sortie.start_fresh_sortie, (), self.sortie_finished)
        self.bee_fresh_sortie.terminate()
        self.bee_resume_sortie = CallbackWorker(self.sortie.resume_sortie, (), self.sortie_finished)
        self.bee_resume_sortie.terminate()

        self.bee_pre_battle.start()

    def on_fresh_sortie(self) -> None:
        reset_sleep_event()
        self._is_speed_mode = False

        self.disable_sortie_widgets()
        self.button_stop_sortie.setEnabled(True)
        self.bee_fresh_sortie.start()

    def on_resume_sortie(self) -> None:
        reset_sleep_event()
        self._is_speed_mode = False

        self.disable_sortie_widgets()
        self.button_stop_sortie.setEnabled(True)
        self.bee_resume_sortie.start()

    def sortie_finished(self, result: bool) -> None:
        self.logger.info('==== Sortie is done! ====')
        self.enable_sortie_widgets()
        self.button_stop_sortie.setEnabled(False)
        if result is True:
            self.logger.debug('sortie success!')
            self.multi_runs.stepDown()
            if self.multi_runs.value() > 0:
                set_sleep()
                self.logger.info('Starting a new run')
                self.bee_fresh_sortie.start()
            else:
                self.logger.info("Completed sortie plan!")
        else:
            self.logger.debug('sortie failed')

        if int(self.ticket_label.text()) == 0:
            self.button_fresh_sortie.setEnabled(False)
            self.button_resume_sortie.setEnabled(False)

    def pre_battle_finished(self, result: bool) -> None:
        if result is True:
            self.logger.info('==== Pre battle checking is done! ====')
        else:
            self.logger.warning('==== Cannot start sortie ====')

    # ================================
    # Update Side Dock
    # ================================

    def update_resources(self, f: int, a: int, s: int, b: int) -> None:
        # signals has to be emitted from a QObject
        self.sig_fuel.emit(f)
        self.sig_ammo.emit(a)
        self.sig_steel.emit(s)
        self.sig_baux.emit(b)

    def update_repair_bucket(self, b):
        self.sig_repair.emit(b)

    def update_user_exp_label(self, x: dict) -> None:
        self.sig_exp.emit(x)

    # ================================
    # Update left-layout display
    # ================================

    def update_ticket(self, data: int) -> None:
        self.ticket_label.setText(str(data))

    def update_purchasable(self, data: int) -> None:
        self.button_purchase.setText(str(data))

    def update_adjutant_name(self, data: str) -> None:
        self.adjutant_label.setText(data)

    def update_adjutant_exp(self, data: str) -> None:
        self.adjutant_exp_label.setText(data)

    def update_points(self, data: str) -> None:
        self.points_label.setText(str(data))

    def update_boat_pool_label(self, data: str) -> None:
        self.boat_pool_label.setText(data)

    def update_fleet_label(self, data: str) -> None:
        self.fleet_label.setText(data)

    # ================================
    # Left Panel - Ship Selection
    # ================================

    def set_ship_selection_buttons(self, dd: list = None, cv: list = None, ss: list = None) -> QWidget:
        def _create_button(t, l, idx, lay, lim=None, cid=None) -> QPushButton:
            b = QPushButton()
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if cid is None:
                b.setText(f'+\n{t}')
            else:
                ship = self.user_ships[str(cid)]
                b.setText(f"{ship['Class']}\n{ship['Name']}\nLv.{ship['Lv.']}")
            b.clicked.connect(lambda _, _i=idx: self.popup_select_window(_i, l, lim))
            lay.addWidget(b)
            self.ship_button_group.addButton(b)
            return b

        w = QWidget()
        v_layout = QVBoxLayout(w)

        row_1 = QHBoxLayout()
        row_1.setContentsMargins(0, 0, 0, 0)
        if dd is not None:
            _create_button(t='LOW COST DD', l=['DD'], idx=0, lay=row_1, lim=[1, 2], cid=dd[0])
            _create_button(t='LOW COST DD', l=['DD'], idx=1, lay=row_1, lim=[1, 2, 3], cid=dd[1])
        else:
            _create_button(t='LOW COST DD', l=['DD'], idx=0, lay=row_1, lim=[1, 2])
            _create_button(t='LOW COST DD', l=['DD'], idx=1, lay=row_1, lim=[1, 2, 3])

        if cv is not None:
            _create_button(t='LOW COST CV/AV', l=['CV', 'AV'], idx=2, lay=row_1, lim=[1, 2, 3], cid=cv[0])
        else:
            _create_button(t='LOW COST CV/AV', l=['CV', 'AV'], idx=2, lay=row_1, lim=[1, 2, 3])

        row_2 = QHBoxLayout()
        row_2.setContentsMargins(0, 0, 0, 0)
        for i in range(3, 9):
            if ss is not None:
                _create_button(t='SS', l=['SS'], idx=i, lay=row_2, cid=ss[i - 3])
            else:
                _create_button(t='SS', l=['SS'], idx=i, lay=row_2)

        v_layout.addLayout(row_1)
        v_layout.addLayout(row_2)
        return w

    def handle_selection(self, ship_info: list, button_id: int) -> None:
        b = self.ship_button_group.buttons()[button_id]
        ship_id = ship_info[1]
        if ship_info[-1] in self.user_chosen_cid:
            b.setText("SHIP EXISTS\nPLEASE CHANGE")
        else:
            self.ship_select_window.close()
            self.ship_select_window.deleteLater()
            self.ship_select_window = None

            self.user_chosen_cid[button_id] = ship_info[-1]
            if button_id in [0, 1]:
                self.escort_DD[button_id] = int(ship_id)
            elif button_id == 2:
                self.escort_CV[0] = int(ship_id)
            else:
                self.battle_fleet[button_id - 3] = int(ship_id)
            s = f'{ship_info[0]}\n{ship_info[2]}\n{ship_info[3]}'
            b.setText(s)

    def popup_select_window(self, btn_id: int, ship_class: list, cost_lim: list = None) -> None:
        self.ship_select_window = ShipSelectWindow(self, btn_id, ship_class, cost_lim)
        self.ship_select_window.show()

    def check_selections(self) -> None:
        try:
            assert (None not in self.escort_DD)
        except AssertionError:
            self.logger.warning('DD are not set')
            return
        try:
            assert (None not in self.escort_CV)
        except AssertionError:
            self.logger.warning('CV are not set')
            return
        try:
            assert (None not in self.battle_fleet)
        except AssertionError:
            self.logger.warning('SS are not set')
            return

        self.button_pre_battle.setEnabled(True)

# End of File
