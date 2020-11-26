import qdarkstyle
import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QHeaderView

from . import constant as SCONST
from ....func import data as wgr_data


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class EquipPopup(QMainWindow):
    def __init__(self, parent, row, col, cid, button_enable):
        super().__init__()
        self.parent = parent
        self._row = row
        self._col = col
        self.cid = int(cid)
        self.button_enable = button_enable

        # TODO hardcoding
        self.width = 600
        self.height = 600
        self.id_list = []
        self.lock_icon = QIcon(get_data_path("src/assets/icons/lock_64.png"))
        self.trans = SCONST._equip_spec

        self.init_ui()
        if self.button_enable == True:
            pass
        else:
            self.button.setEnabled(False)

    def init_ui(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setWindowTitle('WGViewer - Equipment Selection')
        self.resize(self.width, self.height)

        self.button = QPushButton('Unequip Current Equipment')
        self.button.clicked.connect(self.unequip)

        self.tab = QTableWidget()
        self.tab.setColumnCount(4)
        equips = wgr_data.get_ship_equips(self.cid)

        for e in equips:
            self.addTableRow(self.tab, e)
        self.tab.horizontalHeader().setStretchLastSection(True)
        self.tab.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tab.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.tab.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.setHorizontalHeaderLabels(SCONST._equip_header)
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

    def addTableRow(self, table, data):
        self.id_list.append(data['equipmentCid'])
        row = table.rowCount()
        table.setRowCount(row+1)
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

    def get_spec(self, data):
        res = []
        for key in data:
            if not isinstance(data[key], int) or (key == 'star'):
                pass
            elif key == 'range':
                res.append('{}\t{}'.format(self.trans[key], SCONST._range_to_str[data[key]]))
            else:
                res.append('{}\t{}'.format(self.trans[key], data[key]))
        return '\n'.join(res)

    def update_equip(self, index):
        e_id = self.id_list[index.row()]
        self.parent.handle_event(self._row, self._col, e_id)
        self.button.setEnabled(True)

    def unequip(self):
        self.parent.handle_event(self._row, self._col, -1)