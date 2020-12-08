import sys
import os

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QMainWindow,
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHeaderView
)

from src import data as wgv_data
from src.utils.wgv_pyqt import get_user_resolution
from .delegate import ShipTableDelegate
from . import constant as SCONST


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class EquipPopup(QMainWindow):
    def __init__(self, parent: ShipTableDelegate, row: int, col: int, cid: int, button_enable: bool):
        super().__init__()
        self.parent = parent
        self._row = row
        self._col = col
        self.cid = int(cid)
        self.button_enable = button_enable

        user_w, user_h = get_user_resolution()
        self.width = int(user_w * 0.32)
        self.height = int(user_h * 0.55)
        self.id_list = []
        self.lock_icon = QIcon(get_data_path("assets/icons/lock_64.png"))
        self.trans = SCONST.equip_spec

        self.button = QPushButton('Unequip Current Equipment')
        self.tab = QTableWidget()
        self.init_ui()
        if self.button_enable:
            pass
        else:
            self.button.setEnabled(False)

    def init_ui(self) -> None:
        self.setStyleSheet(wgv_data.get_color_scheme())
        self.setWindowTitle('WGViewer - Equipment Selection')
        self.resize(self.width, self.height)

        self.button.clicked.connect(self.unequip)

        self.tab.setColumnCount(4)
        equips = wgv_data.get_ship_equips(self.cid)

        for e in equips:
            self.addTableRow(self.tab, e)
        self.tab.horizontalHeader().setStretchLastSection(True)
        self.tab.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tab.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.tab.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.setHorizontalHeaderLabels(SCONST.equip_header)
        self.tab.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tab.setSelectionBehavior(QTableWidget.SelectRows)
        self.tab.setSelectionMode(QTableWidget.SingleSelection)

        self.tab.doubleClicked.connect(self.update_equip)

        content_layout = QVBoxLayout()

        content_layout.addWidget(self.button)
        content_layout.addWidget(self.tab)
        window = QWidget()
        window.setLayout(content_layout)
        self.setCentralWidget(window)

    def addTableRow(self, table: QTableWidget, data: dict) -> None:
        self.id_list.append(data['equipmentCid'])
        row = table.rowCount()
        table.setRowCount(row + 1)
        # col 0
        title = QTableWidgetItem(data['data']['title'])
        if data['locked'] == 1:
            title.setIcon(self.lock_icon)
        else:
            pass
        table.setItem(row, 0, title)
        # col 1
        table.setItem(row, 1, QTableWidgetItem(str(data['num'])))
        # col 2
        spec = self.get_spec(data['data'])
        table.setItem(row, 2, QTableWidgetItem(spec))
        # col 3
        desc = 'RARITY ' + str(data['data']['star'])
        if data['data']['desc'] == "":
            pass
        else:
            desc += ("\n" + data['data']['desc'])
        table.setItem(row, 3, QTableWidgetItem(desc))

    def get_spec(self, data: dict) -> str:
        res = []
        for key in data:
            if not isinstance(data[key], int) or (key == 'star'):
                pass
            elif key == 'range':
                res.append(f'{self.trans[key]}\t{SCONST.range_to_str[data[key]]}')
            else:
                res.append(f'{self.trans[key]}\t{data[key]}')
        return '\n'.join(res)

    def update_equip(self, index: QModelIndex) -> None:
        e_id = self.id_list[index.row()]
        self.parent.handle_event(self._row, self._col, e_id)
        self.button.setEnabled(True)

    def unequip(self) -> None:
        self.parent.handle_event(self._row, self._col, -1)

# End of File
