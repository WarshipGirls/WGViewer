import logging
import os
import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ResourceTableModel(QAbstractTableModel):
    # https://www.learnpyqt.com/courses/model-views/qtableview-modelviews-numpy-pandas/
    def __init__(self, data):
        super(ResourceTableModel, self).__init__()
        self._data = data

    # ================================
    # Virtual methods
    # ================================

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            return f'{self._data[row][col]:,}'
        if role == Qt.UserRole:
            return self._data[row][col]
        if role == Qt.DecorationRole:
            if row == 0 and col == 0:
                return QIcon(get_data_path('assets/items/fuel.png'))
            elif row == 0 and col == 1:
                return QIcon(get_data_path('assets/items/ammo.png'))
            elif row == 0 and col == 2:
                return QIcon(get_data_path('assets/items/steel.png'))
            elif row == 0 and col == 3:
                return QIcon(get_data_path('assets/items/bauxite.png'))
            elif row == 0 and col == 4:
                return QIcon(get_data_path('assets/items/gold.png'))
            elif row == 1 and col == 0:
                return QIcon(get_data_path('assets/items/instant_repair.png'))
            elif row == 1 and col == 1:
                return QIcon(get_data_path('assets/items/instant_build.png'))
            elif row == 1 and col == 2:
                return QIcon(get_data_path('assets/items/blueprint_construct.png'))
            elif row == 1 and col == 3:
                return QIcon(get_data_path('assets/items/blueprint_dev.png'))
            elif row == 1 and col == 4:
                return QIcon(get_data_path('assets/items/revive.png'))
            elif row == 2 and col == 0:
                return QIcon(get_data_path('assets/items/DD.png'))
            elif row == 2 and col == 1:
                return QIcon(get_data_path('assets/items/CA.png'))
            elif row == 2 and col == 2:
                return QIcon(get_data_path('assets/items/BB.png'))
            elif row == 2 and col == 3:
                return QIcon(get_data_path('assets/items/CV.png'))
            elif row == 2 and col == 4:
                return QIcon(get_data_path('assets/items/SS.png'))
            else:
                logging.error('incorrect indexes')

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        # somehow it can auto format with comma, without explicitly calling Qt.DisplayRole here
        if role == Qt.UserRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, (Qt.UserRole,))
        else:
            return False
        return True

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    # ================================
    # Self Implemented methods
    # ================================
    # TODO: add fade effect
    #  fade a label is quite easy; fade a table cell is not straightforward (maybe need a QThread)
    #  https://python-forum.io/Thread-Change-color-of-a-row-of-a-QTableView
    #  https://stackoverflow.com/questions/48191399/pyqt-fading-a-qlabel
    '''
    old_val = int(self.data(idx, Qt.UserRole))
    # R, G, B, Transparent
    original_color = QColor(0, 0, 0, 255)
    if old_val > new_val:
        # red fade
        new_color = QColor(255, 0, 0, 255)
    elif new_val > old_val:
        # green fade
        new_color = QColor(0, 255, 0, 255)
    else:
        pass
    '''

    @pyqtSlot(int)
    def update_fuel(self, new_val: int):
        idx = self.index(0, 0)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_ammo(self, new_val: int):
        idx = self.index(0, 1)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_steel(self, new_val: int):
        idx = self.index(0, 2)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_bauxite(self, new_val: int):
        idx = self.index(0, 3)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_gold(self, new_val: int):
        idx = self.index(0, 4)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_repair(self, new_val: int):
        idx = self.index(1, 0)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_build(self, new_val: int):
        idx = self.index(1, 1)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_bp_construct(self, new_val: int):
        idx = self.index(1, 2)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_bp_dev(self, new_val: int):
        idx = self.index(1, 3)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_revive(self, new_val: int):
        idx = self.index(1, 4)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_DD(self, new_val: int):
        idx = self.index(2, 0)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_CA(self, new_val: int):
        idx = self.index(2, 1)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_BB(self, new_val: int):
        idx = self.index(2, 2)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_CV(self, new_val: int):
        idx = self.index(2, 3)
        self.setData(idx, new_val, Qt.UserRole)

    @pyqtSlot(int)
    def update_SS(self, new_val: int):
        idx = self.index(2, 4)
        self.setData(idx, new_val, Qt.UserRole)

# End of File
