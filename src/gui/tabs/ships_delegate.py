import qdarkstyle
import sys
import os

from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QStandardItem, QPixmap, QIcon
from PyQt5.QtCore import Qt, QVariant, pyqtSlot, QModelIndex, QRect, pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from . import ships_constant as SCONST
from ...func import data as wgr_data


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class EquipPopup(QMainWindow):
    # ALL temporary, testing
    # TODO: selection signal sent back to main table

    def __init__(self, parent, row, col, cid):
        super().__init__()
        print(self)
        self.parent = parent
        self._row = row
        self._col = col
        self.cid = int(cid)

        self.width = 600
        self.height = 600
        self.id_list = []
        self.lock_icon = QIcon(get_data_path("src/assets/icons/lock_64.png"))
        self.trans = SCONST._equip_spec

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setWindowTitle('WGViewer - Equipment Selection')
        self.resize(self.width, self.height)

        button = QPushButton('Unequip Current Equipment')
        button.clicked.connect(self.button_click_event)

        self.tab = QTableWidget()
        self.tab.setColumnCount(4)
        equips = wgr_data.get_ship_equips(self.cid)
        # print(equips)
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

        self.tab.doubleClicked.connect(self.click_event)

        content_layout = QVBoxLayout()
        # TODO disable button if no equipped
        content_layout.addWidget(button)
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

    def click_event(self, index):
        # index is QModelIndex() object
        e_id = self.id_list[index.row()]
        self.parent.fuck_you(self._row, self._col, e_id)

    def button_click_event(self, index):
        self.parent.fuck_you(self._row, self._col, -1)


class ShipTableDelegate(QStyledItemDelegate):
    def __init__(self, view):
        super().__init__()
        self._view = view

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            # Make only column 1 editable
            return super(ShipTableDelegate, self).createEditor(parent, option, index)
        elif 21 <= index.column() <= 24: 
            # THIS is probably NOT the way it should be done.
            # but I don't know how to do it otherwise
            print("clicked equip " + str(index.row()) + ", " + str(index.column()))
            cid = index.sibling(index.row(), 0).data(Qt.UserRole)
            self._equip_popup(index.row(), index.column(), cid)
        else:
            print("clicked " + str(index.row()) + ", " + str(index.column()))
            # print(index.sibling())

    def setEditorData(self, editor, index):
        print("????????????")

    def setModelData(self, editor, model, index):
        print("!!!!!!!!!!!!!")

    def _equip_popup(self, row, col, cid):
        self.w = EquipPopup(self, row, col, cid)
        self.w.show()

    def fuck_you(self, row, col, eid):
        # the chain of following is disgusting
        self._view.model().sourceModel().update_one_equip(row, col, str(eid))
        self.w.close()


class EquipmentDelegate(QStyledItemDelegate):
    def __init__(self, parent, row, img_path):
        super().__init__(parent)
        self.row = row
        self.img_path = img_path

    # def createEditor(self, parent, option, index):
    #     img = QPixmap()
    #     is_loaded = img.load(self.img_path)
    #     if is_loaded:
    #         l = QLabel(parent)
    #         # thumbnail = QStandardItem()
    #         # thumbnail.setData(QVariant(img), Qt.DecorationRole)
    #         l.setPixmap(img)
    #     else:
    #         pass
    #     return l



# End of File