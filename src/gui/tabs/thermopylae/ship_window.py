import sys
import os

from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import (
    QWidget, QMainWindow,
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHeaderView
)

from src import data as wgv_data
from src.utils import get_user_resolution, get_color_scheme, get_screen_center


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ShipSelectWindow(QMainWindow):
    def __init__(self, parent, button_id: int, ship_class: list, cost_lim: list = None):
        super().__init__()
        self.parent = parent
        self.button_id = button_id
        self.ship_class = ship_class
        self.cost_lim = cost_lim

        self.id_list: list = []
        self.user_ships = wgv_data.get_processed_userShipVo()
        self.id_to_cost = wgv_data.init_ships_temp()

        self.tab = QTableWidget()
        self.init_ui()

    def init_ui(self) -> None:
        self.setStyleSheet(get_color_scheme())
        self.setWindowTitle('WGViewer - Thermopylae')

        self.tab.setColumnCount(4)
        for ship_id, ship in self.user_ships.items():
            self.add_table_row(self.tab, ship_id, ship, self.ship_class, self.cost_lim)

        self.tab.resizeColumnsToContents()
        self.tab.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Level'])
        self.tab.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tab.setSelectionBehavior(QTableWidget.SelectRows)
        self.tab.setSelectionMode(QTableWidget.SingleSelection)

        self.tab.doubleClicked.connect(self.set_ship)

        user_w, user_h = get_user_resolution()
        width = int(0.18 * user_w)
        height = int(0.55 * user_h)
        self.resize(width, height)
        # Following attempts to not block the selection panel
        # TODO? PyQt spawn a new window without blocking the old main window
        #   if old window is in full-screen, then spawn in a fixed position
        new_point = get_screen_center() - self.rect().center()
        self.move(new_point.x() + int(0.1 * user_w), new_point.y())

        content_layout = QVBoxLayout()
        content_layout.addWidget(self.tab)
        window = QWidget()
        window.setLayout(content_layout)
        self.setCentralWidget(window)

    def add_table_row(self, table: QTableWidget, ship_id: int, ship: dict, ship_class: list, cost_lim: list = None) -> None:
        if ship['Class'] not in ship_class:
            return
        else:
            ship_type = ship['Class']
        if int(ship['Lv.']) < 80:
            return
        else:
            ship_lvl = "Lv." + ship['Lv.']
        if cost_lim is not None and self.id_to_cost[str(ship['cid'])]['cost'] not in cost_lim:
            return
        ship_name = ship['Name']
        ship_cid = ship['cid']

        row = table.rowCount()
        table.setRowCount(row + 1)
        table.setItem(row, 0, QTableWidgetItem(ship_type))
        x = QTableWidgetItem()
        x.setData(Qt.DisplayRole, str(ship_id))
        x.setData(Qt.UserRole, ship_cid)
        table.setItem(row, 1, x)
        table.setItem(row, 2, QTableWidgetItem(ship_name))
        table.setItem(row, 3, QTableWidgetItem(ship_lvl))

    def set_ship(self, index: QModelIndex) -> None:
        res = [None] * 4
        for i in range(4):
            res[i] = self.tab.item(index.row(), i).data(Qt.DisplayRole)
        res.append(self.tab.item(index.row(), 1).data(Qt.UserRole))
        self.parent.handle_selection(res, self.button_id)

# End of File
