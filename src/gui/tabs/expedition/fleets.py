from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QTableView, QHeaderView, QAbstractScrollArea, QComboBox, QMainWindow
)

from src import data as wgv_data

# TODO TODO
'''
class PopupFleets(QMainWindow):
    def __init__(self, curr_fleet: list, user_ships: object):
        super().__init__()
        self.curr_fleet = curr_fleet
        self.info = user_ships
        self.width = 400
        self.height = 200

        self.setStyleSheet(wgv_data.get_color_scheme())
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
    def __init__(self):
        super().__init__()

        self.tab = QTableWidget()
        self.tab.setRowCount(28)
        self.tab.setColumnCount(4)

        self.init_ui()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)
        self.maps = wgv_data.get_exp_list()

        self.fleets = wgv_data.get_exp_fleets()
        self.user_ships = wgv_data.get_processed_userShipVo()
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
        print(self.fleets)

        self.set_one_fleet(0, 0, '5')
        self.set_one_fleet(0, 2, '6')
        self.set_one_fleet(14, 0, '7')
        self.set_one_fleet(14, 2, '8')

    def set_one_fleet(self, row: int, col: int, fleet_id: str) -> None:
        fleet_name = "Fleet #" + fleet_id
        item_fleet = QTableWidgetItem(fleet_name)
        item_fleet.setBackground(QColor(0, 0, 0))
        self.tab.setItem(row, col, item_fleet)
        map_name = wgv_data.get_exp_map(fleet_id)
        item_map = QTableWidgetItem(map_name)
        item_map.setBackground(QColor(0, 0, 0))
        self.tab.setItem(row, col + 1, item_map)
        row += 1

        # self.add_button(row, col, 'START', self.start_exp, fleet_id)
        self.add_map_dropdown(row, col)
        self.add_button(row, col + 1, 'STOP (N/A)', self.stop_exp, fleet_id)
        row += 1

        for ship_id in self.fleets[fleet_id]:
            info = self.user_ships[str(ship_id)]
            self.set_one_ship(row, col, ship_id, info)
            row += 2

    def add_button(self, row: int, col: int, text: str, func: Callable, fleet_id: str) -> None:
        w = QWidget()
        b = QPushButton()
        b.setText(text)
        b.clicked.connect(lambda: func(fleet_id))
        l = QHBoxLayout(w)
        l.addWidget(b)
        l.setAlignment(Qt.AlignCenter)
        l.setContentsMargins(0, 0, 0, 0)
        w.setLayout(l)
        self.tab.setCellWidget(row, col, w)

    def add_map_dropdown(self, row: int, col: int) -> None:
        w = QWidget()
        b = QComboBox()
        b.addItems(self.maps)
        t = 'Select Next Expedition Map\n'
        t += '- next one will auto switch after current one is done\n'
        t += '- leave it unchanged for auto-continue'
        b.setToolTip(t)
        l = QHBoxLayout(w)
        l.addWidget(b)
        l.setContentsMargins(0, 0, 0, 0)
        w.setLayout(l)
        self.tab.setCellWidget(row, col, w)

    def set_one_ship(self, row: int, col: int, ship_id: int, info: dict) -> None:
        self.tab.setItem(row, col, QTableWidgetItem(info['Name']))
        s_id = "ID " + str(ship_id)
        self.tab.setItem(row, col + 1, QTableWidgetItem(s_id))
        lvl = "Lv. " + info['Lv.']
        self.tab.setItem(row + 1, col, QTableWidgetItem(lvl))
        self.tab.setItem(row + 1, col + 1, QTableWidgetItem(info['Class']))

    # def start_exp(self, fleet_id: str) -> None:
    #     print(f'{fleet_id} start exp')
    #     print(self.maps)

    def stop_exp(self, fleet_id: str) -> None:
        print(f'{fleet_id} stop exp')
        print(self.maps)

# End of FIle
