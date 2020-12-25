from typing import Callable, List
from logging import Logger

from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QTableView, QHeaderView, QAbstractScrollArea, QComboBox, QButtonGroup
)

from src import utils as wgv_utils
from src.data import get_processed_userShipVo
from src.gui.side_dock.dock import SideDock
from src.gui.side_dock.resource_model import ResourceTableModel
from src.gui.side_dock.constants import EXP_LABEL_R

BTN_TEXT_START: str = 'START'
BTN_TEXT_STOP: str = 'STOP'

# TODO: user select fleet
# TODO: auto switch exp map

'''
class PopupFleets(QMainWindow):
    def __init__(self, curr_fleet: list, user_ships: object):
        super().__init__()
        self.curr_fleet = curr_fleet
        self.info = user_ships
        self.width = 400
        self.height = 200

        self.setStyleSheet(wgv_utils.get_color_scheme())
        self.setWindowTitle('WGViewer - Expedition Fleet Selection')
        self.resize(self.width, self.height)

        content_layout = QVBoxLayout()

        self.tab = QTableWidget()
        self.tab.setRowCount(7)
        for ship_id in self.curr_fleet:
            info = self.info[str(ship_id)]
            self.set_one_ship(row, ship_id, info)

    def set_one_ship(self, row, ship_id, info):
        self.tab.setItem(row, 0, QTableWidgetItem(info['Name']))
        self.tab.setItem()
'''


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


class ExpFleets(QWidget):
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

        self.tab = QTableWidget()
        self.layout = QVBoxLayout(self)
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
        self.tab.setRowCount(28)
        self.tab.setColumnCount(4)
        self.tab.resizeColumnsToContents()
        self.tab.resizeRowsToContents()
        self.tab.setShowGrid(False)
        self.tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().hide()
        self.tab.verticalHeader().hide()
        self.tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.setEditTriggers(QTableView.NoEditTriggers)
        self.tab.setFocusPolicy(Qt.NoFocus)
        self.tab.setSelectionMode(QTableView.NoSelection)
        self.tab.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)

    def get_row_count(self) -> int:
        return self.tab.rowCount()

    def get_col_count(self) -> int:
        return self.tab.columnCount()

    def set_table(self) -> None:
        self.set_one_fleet(0, 0, '5')
        self.set_one_fleet(0, 2, '6')
        self.set_one_fleet(14, 0, '7')
        self.set_one_fleet(14, 2, '8')

    def set_one_fleet(self, row: int, col: int, fleet_id: str) -> None:
        fleet_name = "Fleet #" + fleet_id
        item_fleet = QTableWidgetItem(fleet_name)
        item_fleet.setBackground(QColor(0, 0, 0))
        self.tab.setItem(row, col, item_fleet)
        map_name = wgv_utils.get_exp_map(fleet_id)
        item_map = QTableWidgetItem(map_name)
        item_map.setBackground(QColor(0, 0, 0))
        self.tab.setItem(row, col + 1, item_map)
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
        self.tab.setCellWidget(row, col, w)

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
        self.tab.setCellWidget(row, col, w)

    def on_dropdown_change(self, fleet_idx: int, next_map: str) -> None:
        self.next_exp_maps[fleet_idx] = next_map
        self.logger.debug(f"Next expedition map changed: {self.next_exp_maps}")

    def set_one_ship(self, row: int, col: int, ship_id: int, info: dict) -> None:
        self.tab.setItem(row, col, QTableWidgetItem(info['Name']))
        s_id = "ID " + str(ship_id)
        self.tab.setItem(row, col + 1, QTableWidgetItem(s_id))
        lvl = "Lv. " + info['Lv.']
        self.tab.setItem(row + 1, col, QTableWidgetItem(lvl))
        self.tab.setItem(row + 1, col + 1, QTableWidgetItem(info['Class']))

    def on_button_clicked(self, fleet_idx: int) -> None:
        # TODO: check if fleet class requirement met
        btn = self.exp_buttons.buttons()[fleet_idx]
        curr_map = self.curr_exp_maps[fleet_idx].replace('-', '000')
        if btn.text() == BTN_TEXT_START:
            self.logger.info(f'fleet #{fleet_idx + 5} start expedition on {self.next_exp_maps[fleet_idx]}')
            next_map = self.next_exp_maps[fleet_idx].replace('-', '000')
            fleet_id = str(fleet_idx + 5)
            if self.get_counter_label(fleet_idx) == EXP_LABEL_R:  # if idling
                pass
            else:
                self._get_exp_result(curr_map)
            start_res = self._start_exp(next_map, fleet_id)
            d = next((i for i in start_res['pveExploreVo']['levels'] if i['fleetId'] == fleet_id))
            self._update_one_expedition(d)

            btn.setText(BTN_TEXT_STOP)
            self.curr_exp_maps[fleet_idx] = self.next_exp_maps[fleet_idx]
        elif btn.text() == BTN_TEXT_STOP:
            self.logger.info(f'fleet #{fleet_idx + 5} stops expedition on {self.next_exp_maps[fleet_idx]}')
            self._cancel_exp(curr_map, fleet_idx)
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

    def _get_exp_result(self, curr_map: str) -> None:
        # TODO: updateTaskVo
        res = self.side_dock.exp_list_view.get_exp_result(curr_map)
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

    def _start_exp(self, next_map: str, fleet_id: str) -> dict:
        return self.side_dock.exp_list_view.start_exp(next_map, fleet_id)

    def _cancel_exp(self, exp_map: str, fleet_idx: int) -> dict:
        self.side_dock.cancel_one_expedition(fleet_idx)
        return self.side_dock.exp_list_view.cancel_exp(exp_map)

    def _update_one_expedition(self, data: dict) -> None:
        self.side_dock.update_one_expedition(data)

# End of FIle
