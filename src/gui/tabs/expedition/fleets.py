import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QTableView, QHeaderView, QAbstractScrollArea
)

from src import data as wgr_data


class ExpFleets(QWidget):
    def __init__(self):
        super().__init__()

        self.tab = QTableWidget()
        self.tab.setRowCount(33)
        self.tab.setColumnCount(4)
        for i in range(self.tab.rowCount()):
            for j in range(self.tab.rowCount()):
                self.tab.setItem(i, j, QTableWidgetItem(str([i, j, i, j, i, j])))

        # self.tab = QTableWidget()
        # self.tab.setColumnCount()

        # # f1 = OneExpFleet()
        self.init_ui()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)

        self.fleets = wgr_data.get_exp_fleets()
        self.ships_info = wgr_data.get_processed_userShipVo()
        self.set_table()

    def init_ui(self):
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

    def get_row_count(self):
        return self.tab.rowCount()

    def get_col_count(self):
        return self.tab.columnCount()

    def set_table(self):
        print(self.fleets)

        self.set_one_fleet(1, 0, '5')
        self.set_one_fleet(1, 2, '6')
        self.set_one_fleet(17, 0, '7')
        self.set_one_fleet(17, 2, '8')

    def set_one_fleet(self, row, col, fleet_id):
        fleet_name = "Fleet #" + fleet_id
        self.tab.setItem(row, col, QTableWidgetItem(fleet_name))
        row += 1

        self.add_button(row, col, 'START', self.start_exp, fleet_id)
        self.add_button(row, col + 1, 'STOP', self.stop_exp, fleet_id)
        row += 1

        for ship_id in self.fleets[fleet_id]:
            info = self.ships_info[str(ship_id)]
            self.set_one_ship(row, col, ship_id, info)
            row += 2

    def add_button(self, row, col, text, func, fleet_id):
        w = QWidget()
        b = QPushButton()
        b.setText(text)
        b.clicked.connect(lambda: func(fleet_id))
        l = QHBoxLayout(w)
        l.addWidget(b)
        l.setAlignment(Qt.AlignCenter)
        l.setContentsMargins(0, 0, 0, 0)
        w.setLayout(l)
        # self.buttons.append(b)
        self.tab.setCellWidget(row, col, w)

    def set_one_ship(self, row, col, ship_id, info):
        self.tab.setItem(row, col, QTableWidgetItem(info['Name']))
        self.tab.setItem(row, col + 1, QTableWidgetItem(str(ship_id)))
        self.tab.setItem(row + 1, col, QTableWidgetItem(info['Lv.']))
        self.tab.setItem(row + 1, col + 1, QTableWidgetItem(info['Class']))

    def start_exp(self, fleet_id):
        print(f'{fleet_id} start exp')

    def stop_exp(self, fleet_id):
        print(f'{fleet_id} stop exp')

# End of FIle
