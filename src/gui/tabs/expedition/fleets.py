from typing import Callable, List, Tuple
from logging import Logger

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QTableView, QHeaderView, QAbstractScrollArea, QComboBox, QMainWindow, QButtonGroup
)

from src import utils as wgv_utils
from src.data import get_processed_userShipVo, load_cookies
from src.exceptions.wgr_error import get_error, WarshipGirlsExceptions
from src.gui.side_dock.dock import SideDock
from src.wgr import API_EXPLORE

BTN_TEXT_START: str = 'START'
BTN_TEXT_STOP: str = 'STOP'

# TODO: manually start expedition
# TODO: manually get result
# TODO: update side dock based on manual call response
# TODO: From side dock call the tab?
#    - but how? chicken vs egg?
# TODO: auto start expedition
# TODO: auto get result
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


class ExpFleets(QWidget):
    def __init__(self, side_dock: SideDock, logger: Logger):
        super().__init__()
        self.side_dock = side_dock
        self.logger = logger

        self.tab = QTableWidget()
        self.tab.setRowCount(28)
        self.tab.setColumnCount(4)

        self.api = API_EXPLORE(load_cookies())

        self.init_ui()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)
        self.maps = wgv_utils.get_exp_list()
        self.curr_exp_maps: List[str] = ['', '', '', '']
        self.next_exp_maps: List[str] = ['', '', '', '']
        self.exp_buttons = QButtonGroup()

        self.reconnection_limit = 3
        self.fleets = wgv_utils.get_exp_fleets()
        self.user_ships = get_processed_userShipVo()
        self.set_table()

    def init_ui(self) -> None:
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
        if self.get_left_time(fleet_idx) > 0:
            button_text = BTN_TEXT_STOP
        else:
            # TODO: if not collected collects the reward, then start
            button_text = BTN_TEXT_START
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
        b = QComboBox()
        b.addItems(self.maps)
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

    def on_dropdown_change(self, fleet: int, next_map: str) -> None:
        self.logger.debug(f"Next expedition map changed: {self.next_exp_maps}")
        self.next_exp_maps[fleet] = next_map

    def set_one_ship(self, row: int, col: int, ship_id: int, info: dict) -> None:
        self.tab.setItem(row, col, QTableWidgetItem(info['Name']))
        s_id = "ID " + str(ship_id)
        self.tab.setItem(row, col + 1, QTableWidgetItem(s_id))
        lvl = "Lv. " + info['Lv.']
        self.tab.setItem(row + 1, col, QTableWidgetItem(lvl))
        self.tab.setItem(row + 1, col + 1, QTableWidgetItem(info['Class']))

    def on_button_clicked(self, fleet_idx: int) -> None:
        self.logger.debug(f'fleet #{fleet_idx + 5} shall start{self.next_exp_maps[fleet_idx]}')
        # TODO: check if fleet class requirement met
        b = self.exp_buttons.buttons()[fleet_idx]
        if b.text() == BTN_TEXT_START:
            curr_map = self.curr_exp_maps[fleet_idx].replace('-', '000')
            next_map = self.next_exp_maps[fleet_idx].replace('-', '000')
            fleet_id = str(fleet_idx + 5)

            res_res = self.get_exp_result(curr_map)
            start_res = self.start_exp(next_map, fleet_id)
            self.logger.debug(res_res)
            self.logger.debug(start_res)
        elif b.text() == BTN_TEXT_STOP:
            self.logger.debug('stop expedition')
        else:
            pass

    def get_left_time(self, fleet_idx: int) -> int:
        return self.side_dock.get_exp_counters()[fleet_idx]

    def _reconnecting_calls(self, func: Callable, func_info: str) -> [dict, object]:
        # This redundancy while-loop (compared to api.py's while-loop) deals with WarshipGirlsExceptions;
        #   while the other one deals with URLError etc
        res = False  # status
        data = None
        tries = 0
        while not res:
            try:
                self.logger.debug(f"{func_info}...")
                res, data = func()
            except WarshipGirlsExceptions as e:
                self.logger.warning(f"Failed to {func_info} due to {e}. Trying reconnecting...")
                wgv_utils.set_sleep()
            tries += 1
            if tries >= self.reconnection_limit:
                break
            else:
                pass
        return data

    def get_exp_result(self, exp_map: str) -> dict:
        def _get_res() -> Tuple[bool, dict]:
            data = self.api.getResult(exp_map)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'pveExploreVo' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_get_res, 'collect expedition')

    def start_exp(self, exp_map: str, fleet_id: str) -> dict:
        def _start() -> Tuple[bool, dict]:
            data = self.api.start(exp_map, fleet_id)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'pveExploreVo' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_start, 'start expedition')

# End of FIle
