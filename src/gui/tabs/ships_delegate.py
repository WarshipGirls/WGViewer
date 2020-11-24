import qdarkstyle
import sys
import os

from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QStandardItem, QPixmap, QIcon
from PyQt5.QtCore import Qt, QVariant, pyqtSlot, QModelIndex, QRect, pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from ...func import data as wgr_data


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class EquipPopup(QMainWindow):
    # ALL temporary, testing
    resized = pyqtSignal()
    def __init__(self, cid, parent=None):
        super().__init__()
        self.width = 600
        self.height = 600
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setWindowTitle('WGViewer - Equipment Selection')
        self.resize(self.width, self.height)
        self.lock_icon = QIcon(get_data_path("src/assets/icons/lock_64.png"))
        self.cid = int(cid)
        equips = wgr_data.get_ship_equips(self.cid)

        self.tab = QTableWidget(self)
        self.tab.setColumnCount(4)
        for e in equips:
            self.addTableRow(self.tab, e)
        #Table will fit the screen horizontally 
        self.tab.horizontalHeader().setStretchLastSection(True) 
        self.tab.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tab.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().hide()
        self.tab.resize(self.width, self.height)
        self.tab.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.resized.connect(self.resize_table)

    def addTableRow(self, table, data):
        row = table.rowCount()
        table.setRowCount(row+1)

        title = QTableWidgetItem(data['data']['title'])
        if data['locked'] == 1:
            title.setIcon(self.lock_icon)
        else:
            pass
        table.setItem(row, 0, title)
        table.setItem(row, 1, QTableWidgetItem(str(data['num'])))
        spec = self.get_spec(data['data'])
        table.setItem(row, 2, QTableWidgetItem(spec))

        desc = 'RARITY ' + str(data['data']['star'])
        if data['data']['desc'] == "":
            pass
        else:
            desc += ("\n" + data['data']['desc'])

        table.setItem(row, 3, QTableWidgetItem(desc))

    def get_spec(self, data):
        res = []
        for key in data:
            if not isinstance(data[key], int):
                pass
            else:
                res.append('{}\t{}'.format(key, data[key]))
        return '\n'.join(res)

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def resize_table(self):
        # TODO: this not working
        self.tab.setGeometry(0, 0, self.width, self.height)


class ShipTableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Make only column 1 editable
        if index.column() == 1:
            return super(ShipTableDelegate, self).createEditor(parent, option, index)
        elif 21 <= index.column() <= 24: 
            print("clicked equip " + str(index.row()) + ", " + str(index.column()))
            cid = index.sibling(index.row(), 0).data(Qt.UserRole)
            self.popup(cid)
        else:
            print("clicked " + str(index.row()) + ", " + str(index.column()))
            # print(index.sibling())

    def setEditorData(self, editor, index):
        print("????????????")

    def setModelData(self, editor, model, index):
        print("!!!!!!!!!!!!!")

    def popup(self, cid):
        self.w = EquipPopup(cid)
        self.w.show()


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