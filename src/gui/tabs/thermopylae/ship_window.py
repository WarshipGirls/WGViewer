import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import (
    QWidget, QMainWindow,
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHeaderView
)

from src import data as wgv_data
from src.utils.wgv_pyqt import get_user_resolution


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ShipSelectWindow(QMainWindow):
    def __init__(self, parent, button_id):
        super().__init__()
        self.parent = parent
        self.button_id = button_id

        user_w, user_h = get_user_resolution()
        self.width = int(0.16 * user_w)
        self.height = int(0.55 * user_h)
        self.id_list = []
        self.ships_info = None
        self.lock_icon = QIcon(get_data_path("assets/icons/lock_64.png"))

        self.tab = QTableWidget()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(wgv_data.get_color_scheme())
        self.setWindowTitle('WGViewer - Ship Selection')
        self.resize(self.width, self.height)

        self.tab.setColumnCount(4)
        # TODO remove Lv. 1 ships; add a label to inform user this
        self.ships_info = wgv_data.get_processed_userShipVo()
        for ship_id, ship in self.ships_info.items():
            self.add_table_row(self.tab, ship_id, ship)

        # self.tab.horizontalHeader().setStretchLastSection(True)
        self.tab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.tab.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Level'])
        self.tab.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tab.setSelectionBehavior(QTableWidget.SelectRows)
        self.tab.setSelectionMode(QTableWidget.SingleSelection)

        self.tab.doubleClicked.connect(self.set_ship)

        content_layout = QVBoxLayout()

        content_layout.addWidget(self.tab)
        window = QWidget()
        window.setLayout(content_layout)
        self.setCentralWidget(window)

    @staticmethod
    def add_table_row(table, ship_id, ship):
        ship_name = ship['Name']
        ship_type = ship['Class']
        ship_lvl = "Lv." + ship['Lv.']

        row = table.rowCount()
        table.setRowCount(row + 1)
        table.setItem(row, 0, QTableWidgetItem(ship_type))
        table.setItem(row, 1, QTableWidgetItem(str(ship_id)))
        table.setItem(row, 2, QTableWidgetItem(ship_name))
        table.setItem(row, 3, QTableWidgetItem(ship_lvl))

    def set_ship(self, index: QModelIndex):
        res = [None] * 4
        for i in range(4):
            res[i] = self.tab.item(index.row(), i).data(Qt.DisplayRole)
        self.parent.handle_selection(res, self.button_id)

# End of File
