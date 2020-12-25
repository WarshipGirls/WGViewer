from typing import Callable, List, Tuple
from logging import Logger

from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QTableView, QHeaderView, QAbstractScrollArea, QComboBox, QButtonGroup, QMainWindow, QLabel
)

from src import utils as wgv_utils
from src.data import get_processed_userShipVo
from src.func.worker import CallbackWorker
from src.gui.side_dock.dock import SideDock
from src.gui.side_dock.resource_model import ResourceTableModel
from src.gui.side_dock.constants import EXP_LABEL_R

BTN_TEXT_START: str = 'START'
BTN_TEXT_STOP: str = 'STOP'

# TODO: user select fleet
# TODO: refactor
# TODO: use a worker thread for api calls
# TODO: if auto-on, the original start_expedition not working, triple start calls
#   correct procedure is get result then start; manual works

"""
fleet_id, str, represents '5', '6', '7', '8'
fleet_idx, int, represents 0, 1, 2, 3

Lesson: Basic rule of Qt and PyQt, the GUI is never modified from another thread other than the main thread,
    the main thread is called the GUI thread!!!! – eyllanesc
"""


class PopupFleets(QMainWindow):
    def __init__(self, fleet_id: str):
        super().__init__()
        self.fleet = wgv_utils.get_exp_fleets()[fleet_id]
        self.user_ships = get_processed_userShipVo()

        self.setStyleSheet(wgv_utils.get_color_scheme())
        self.setWindowTitle('WGViewer - Expedition Fleet Selection')
        self.width = 200
        self.height = 500
        self.resize(self.width, self.height)

        self.curr_tab = QTableWidget()
        self.next_buttons = QButtonGroup()
        self.set_curr_table(0)

        content_layout_widget = QWidget(self)
        content_layout = QVBoxLayout(content_layout_widget)
        content_layout.addWidget(QLabel(f'Current Fleet {fleet_id}'))
        content_layout.addWidget(self.curr_tab)
        content_layout.addWidget(QLabel(f'Expedition Fleet for Next Map'))
        for b in self.next_buttons.buttons():
            content_layout.addWidget(b)
        self.setCentralWidget(content_layout_widget)

        self.show()

    def set_curr_table(self, row: int) -> None:
        self.curr_tab.setRowCount(6)
        self.curr_tab.setColumnCount(3)
        for ship_id in self.fleet:
            info = self.user_ships[str(ship_id)]
            self.curr_tab.setItem(row, 0, QTableWidgetItem(info['Class']))
            self.curr_tab.setItem(row, 1, QTableWidgetItem(info['Lv.']))
            self.curr_tab.setItem(row, 2, QTableWidgetItem(info['Name']))
            row += 1
        self.curr_tab.resizeColumnsToContents()
        self.curr_tab.resizeRowsToContents()
        self.curr_tab.setShowGrid(False)
        self.curr_tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.curr_tab.horizontalHeader().hide()
        self.curr_tab.verticalHeader().hide()
        self.curr_tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.curr_tab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.curr_tab.setEditTriggers(QTableView.NoEditTriggers)
        self.curr_tab.setFocusPolicy(Qt.NoFocus)
        self.curr_tab.setSelectionMode(QTableView.NoSelection)
        self.curr_tab.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def set_next_table(self) -> None:
        # TODO: like ship_window.py
        pass


class CustomComboBox(QComboBox):
    """
    QComboBox that can enable/disable certain items.
        Rendering dropdown items upon clicking
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.maps = wgv_utils.get_exp_list()
        self.addItems(self.maps)
        self.installEventFilter(self)

    def eventFilter(self, target, event):
        if target == self and event.type() == QEvent.MouseButtonPress:
            self.disable_maps()
        return False

    def disable_maps(self):
        for i in range(self.count()):
            item = self.model().item(i)
            item.setEnabled(item.text() not in self.parent.next_exp_maps)


class ExpFleets(QTableWidget):
    sig_fuel = pyqtSignal(int)
    sig_ammo = pyqtSignal(int)
    sig_steel = pyqtSignal(int)
    sig_baux = pyqtSignal(int)
    sig_repair = pyqtSignal(int)
    sig_build = pyqtSignal(int)
    sig_bp_construct = pyqtSignal(int)
    sig_bp_dev = pyqtSignal(int)
    sig_exp = pyqtSignal(dict)

    def __init__(self, side_dock: SideDock, summary, logger: Logger):
        super().__init__()
        self.side_dock = side_dock
        self.summary = summary
        self.logger = logger

        for x in wgv_utils.welcome_console_message():
            self.logger.info(x)
        del x

        self.resource_info: ResourceTableModel = self.side_dock.table_model

        # Signals
        self.sig_fuel.connect(self.resource_info.update_fuel)
        self.sig_ammo.connect(self.resource_info.update_ammo)
        self.sig_steel.connect(self.resource_info.update_steel)
        self.sig_baux.connect(self.resource_info.update_bauxite)
        self.sig_repair.connect(self.resource_info.update_repair)
        self.sig_build.connect(self.resource_info.update_build)
        self.sig_bp_construct.connect(self.resource_info.update_bp_construct)
        self.sig_bp_dev.connect(self.resource_info.update_bp_dev)
        self.sig_exp.connect(self.side_dock.update_lvl_label)

        self.init_ui()

        self.exp_buttons = QButtonGroup()
        self.fleets = wgv_utils.get_exp_fleets()
        self.user_ships = get_processed_userShipVo()
        self.curr_exp_maps: List[str] = ['1-1'] * 4
        self.next_exp_maps: List[str] = ['1-1'] * 4

        self.set_table()

    # ================================
    # UI
    # ================================

    def init_ui(self) -> None:
        self.setRowCount(28)
        self.setColumnCount(4)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setShowGrid(False)
        # Keep following one; it differs from resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QTableView.NoSelection)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def set_table(self) -> None:
        self.set_one_fleet(0, 0, '5')
        self.set_one_fleet(0, 2, '6')
        self.set_one_fleet(14, 0, '7')
        self.set_one_fleet(14, 2, '8')

    def set_one_fleet(self, row: int, col: int, fleet_id: str) -> None:
        fleet_name = "Fleet #" + fleet_id
        item_fleet = QTableWidgetItem(fleet_name)
        item_fleet.setBackground(QColor(0, 0, 0))
        self.setItem(row, col, item_fleet)
        map_name = wgv_utils.get_exp_map(fleet_id)
        item_map = QTableWidgetItem(map_name)
        item_map.setBackground(QColor(0, 0, 0))
        self.setItem(row, col + 1, item_map)
        row += 1

        fleet_idx = int(fleet_id) - 5
        self.next_exp_maps[fleet_idx] = map_name
        self.curr_exp_maps[fleet_idx] = map_name
        self.add_map_dropdown(row, col, fleet_idx, map_name)
        left_time = self.get_left_time(fleet_idx)
        if left_time is None or left_time <= 0:
            button_text = BTN_TEXT_START
        else:
            button_text = BTN_TEXT_STOP
        self.add_button(row, col + 1, button_text, self.on_button_clicked, fleet_idx)
        row += 1

        for ship_id in self.fleets[fleet_id]:
            info = self.user_ships[str(ship_id)]
            self.set_one_ship(row, col, ship_id, info)
            row += 2

    def add_button(self, row: int, col: int, text: str, func: Callable, fleet_idx: int) -> None:
        w = QWidget()
        b = QPushButton()
        b.setText(text)
        b.clicked.connect(lambda: func(fleet_idx))
        self.exp_buttons.addButton(b)
        l = QHBoxLayout(w)
        l.addWidget(b)
        l.setAlignment(Qt.AlignCenter)
        l.setContentsMargins(0, 0, 0, 0)
        w.setLayout(l)
        self.setCellWidget(row, col, w)

    def add_map_dropdown(self, row: int, col: int, fleet_idx: int, map_name: str) -> None:
        w = QWidget()
        b = CustomComboBox(self)
        t = 'Select Next Expedition Map\n'
        t += '- next one will auto switch after current one is done\n'
        t += '- leave it unchanged for auto-continue'
        b.setToolTip(t)
        b.currentIndexChanged.connect(lambda _, _b=b: self.on_dropdown_change(fleet_idx, _b.currentText()))
        b.setCurrentText(map_name)
        l = QHBoxLayout(w)
        l.addWidget(b)
        l.setContentsMargins(0, 0, 0, 0)
        w.setLayout(l)
        self.setCellWidget(row, col, w)

    def on_dropdown_change(self, fleet_idx: int, next_map: str) -> None:
        self.next_exp_maps[fleet_idx] = next_map
        self.logger.debug(f"Next expedition map changed: {self.next_exp_maps}")

    def set_one_ship(self, row: int, col: int, ship_id: int, info: dict) -> None:
        self.setItem(row, col, QTableWidgetItem(info['Name']))
        s_id = "ID " + str(ship_id)
        self.setItem(row, col + 1, QTableWidgetItem(s_id))
        lvl = "Lv. " + info['Lv.']
        self.setItem(row + 1, col, QTableWidgetItem(lvl))
        self.setItem(row + 1, col + 1, QTableWidgetItem(info['Class']))

    def start_expedition(self, fleet_idx: int) -> Tuple[dict, int]:
        """
        Start an expedition.
            - side_dock.exp_list_view also has access to this method
        @param fleet_idx: the 0-based fleet index
        @type fleet_idx: int
        @return: None
        @rtype: None
        """

        next_map = self.next_exp_maps[fleet_idx].replace('-', '000')
        fleet_id = str(fleet_idx + 5)
        start_res = self._start_exp(next_map, fleet_id)
        return start_res, fleet_idx

    def on_start_expedition_finished(self, result: Tuple[dict, int]) -> None:
        start_res = result[0]
        if start_res is None:
            return
        fleet_idx = result[1]
        fleet_id = str(fleet_idx + 5)
        d = next((i for i in start_res['pveExploreVo']['levels'] if i['fleetId'] == fleet_id))
        self._update_one_expedition(d)

        button = self.exp_buttons.buttons()[fleet_idx]
        button.setText(BTN_TEXT_STOP)
        self.curr_exp_maps[fleet_idx] = self.next_exp_maps[fleet_idx]
        item_map = QTableWidgetItem(self.curr_exp_maps[fleet_idx])
        item_map.setBackground(QColor(0, 0, 0))
        if fleet_idx == 0:
            self.setItem(0, 1, item_map)
        elif fleet_idx == 1:
            self.setItem(0, 3, item_map)
        elif fleet_idx == 2:
            self.setItem(14, 1, item_map)
        elif fleet_idx == 3:
            self.setItem(14, 3, item_map)
        else:
            pass

    def stop_expedition(self, curr_map: str, fleet_idx: int) -> int:
        self._cancel_exp(curr_map, fleet_idx)
        return fleet_idx

    def on_stop_expedition_finished(self, fleet_idx: int) -> None:
        self.side_dock.cancel_one_expedition(fleet_idx)

    def on_button_clicked(self, fleet_idx: int, is_auto: bool = False) -> None:
        # TODO: check if fleet class requirement met
        btn = self.exp_buttons.buttons()[fleet_idx]
        if btn.text() == BTN_TEXT_START or is_auto is True:
            self.logger.info(f'fleet #{fleet_idx + 5} start expedition on {self.next_exp_maps[fleet_idx]}')

            # self.start_expedition(fleet_idx)
            curr_map = self.curr_exp_maps[fleet_idx].replace('-', '000')
            self.bee_start = CallbackWorker(self.start_expedition, ([fleet_idx]), self.on_start_expedition_finished)
            self.bee_start.terminate()
            self.bee_res = CallbackWorker(self._get_exp_result, ([curr_map, fleet_idx]), self.on_get_result_finished)
            self.bee_res.terminate()
            if self.get_counter_label(fleet_idx) == EXP_LABEL_R:  # if idling
                self.bee_start.start()
            else:
                self.bee_res.start()
                # self._get_exp_result(curr_map)
        elif btn.text() == BTN_TEXT_STOP:
            self.logger.info(f'fleet #{fleet_idx + 5} stops expedition on {self.next_exp_maps[fleet_idx]}')
            curr_map = self.curr_exp_maps[fleet_idx].replace('-', '000')
            self.bee_stop = CallbackWorker(self.stop_expedition, (curr_map, fleet_idx), self.on_stop_expedition_finished)
            self.bee_stop.terminate()
            self.bee_stop.start()
            btn.setText(BTN_TEXT_START)
        else:
            pass

    # ================================
    # Signals
    # ================================

    def update_resources(self, user_res_vo: dict) -> None:
        # signals has to be emitted from a QObject
        f = user_res_vo['oil']
        a = user_res_vo['ammo']
        s = user_res_vo['steel']
        b = user_res_vo['aluminium']
        self.sig_fuel.emit(f)
        self.sig_ammo.emit(a)
        self.sig_steel.emit(s)
        self.sig_baux.emit(b)

    # ================================
    # SideDock methods
    # ================================

    def get_left_time(self, fleet_idx: int) -> int:
        return self.side_dock.exp_list_view.get_counters()[fleet_idx]

    def get_counter_label(self, fleet_idx: int) -> str:
        l = [i.text() for i in self.side_dock.exp_list_view.get_counter_labels()]
        return l[fleet_idx]

    def _get_exp_result(self, curr_map: str, fleet_idx: int) -> Tuple[dict, int]:
        res = self.side_dock.exp_list_view.get_exp_result(curr_map)
        return res, fleet_idx

    def on_get_result_finished(self, result: Tuple[dict, int]) -> None:
        res = result[0]
        # TODO: updateTaskVo
        self.sig_exp.emit(res['userLevelVo'])
        success_str = "big success" if res['bigSuccess'] == 1 else "success"
        self.logger.info(success_str)

        # update reward items
        if 'packageVo' not in res:
            pass
        else:
            for item in res['packageVo']:
                if item['itemCid'] == 541:
                    self.sig_repair.emit(item['num'])
                elif item['itemCid'] == 141:
                    self.sig_build.emit(item['num'])
                elif item['itemCid'] == 241:
                    self.sig_bp_construct.emit(item['num'])
                elif item['itemCid'] == 741:
                    self.sig_bp_dev.emit(item['num'])
                else:
                    self.logger.debug('unprocessed item cid')
        # update resources
        self.update_resources(res['userResVo'])
        # update summary table
        self.summary.on_newAward(res['newAward'])

        fleet_idx = result[1]
        # self.bee_start = CallbackWorker(self.start_expedition, ([fleet_idx]), self.on_start_expedition_finished)
        # self.bee_start.terminate()
        self.bee_start.start()

    def _start_exp(self, next_map: str, fleet_id: str) -> dict:
        return self.side_dock.exp_list_view.start_exp(next_map, fleet_id)

    def _cancel_exp(self, exp_map: str, fleet_idx: int) -> dict:
        return self.side_dock.exp_list_view.cancel_exp(exp_map)

    def _update_one_expedition(self, data: dict) -> None:
        self.side_dock.update_one_expedition(data)

# End of FIle
