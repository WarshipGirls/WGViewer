from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QStandardItem, QPixmap
from PyQt5.QtCore import Qt, QVariant, pyqtSlot, QModelIndex, QRect
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow

import qdarkstyle

class EquipPopup(QMainWindow):
    def __init__(self, cid, parent=None):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setWindowTitle('WGViewer - Equipment Selection')
        self.resize(400, 400)


        '''
        1. get current cid
        2. get corresponding equipmentType in shipCard by cid
        3. get all equipment id in shipEquipmnt (yes, no 'e')
        4. get all user-owned equipment by equipment id
        '''
        self.cid = cid


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