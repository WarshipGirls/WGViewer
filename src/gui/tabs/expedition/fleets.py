import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractScrollArea

from ....data import data as wgr_data


class ExpFleets(QWidget):
    def __init__(self):
        super().__init__()

        self.tab = QTableWidget()
        self.tab.setRowCount(33)
        self.tab.setColumnCount(4)
        for i in range(self.tab.rowCount()):
            for j in range(self.tab.rowCount()):
                self.tab.setItem(i,j,QTableWidgetItem(str([i,j,i,j,i,j])))

        # self.tab = QTableWidget()
        # self.tab.setColumnCount()

        # # f1 = OneExpFleet()
        self.init_ui()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)

        self.get_fleets()

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

    def get_fleets(self):
        self.fleets = wgr_data.get_exp_fleets()
        self.ships_info = wgr_data.get_processed_userShipVo()
        # print(self.ships_info)
        for fleet_id in self.fleets:
            for ship_id in self.fleets[fleet_id]:
                try:
                    info = self.ships_info[str(ship_id)]
                    # TODO show data on the table
                    print(info['Name'], ship_id, info['Lv.'], info['Class'])
                except KeyError as e:
                    logging.error(e)


# End of FIle