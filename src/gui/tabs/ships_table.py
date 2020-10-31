import sys
import os
import logging

from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from ...func.helper_function import Helper
from ...func import constants as CONST

def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ShipTableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Make only column 1 editable
        if index.column() == 1:
            return super(ShipTableDelegate, self).createEditor(parent, option, index)
        else:
            print("clicked " + str(index.column()))


class ShipTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.hlp = Helper()
        self.setItemDelegate(ShipTableDelegate(self))
        # TODO: https://github.com/ColinDuquesnoy/QDarkStyleSheet/issues/245
        self.headers = ["", "Name", "ID", "Class", "Lv.", "HP", "Torp.", "Eva.", "Range", "ASW", "AA", "Fire.", "Armor", "Luck", "LOS", "Speed", "Slot", "Equip.", "Tact."]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

        self.setShowGrid(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ships_S = []
        self.ships_M = []
        self.ships_L = []
        self.non_mods = []
        self.mods = []

    def add_ship(self, row, data):
        self.set_thumbnail(row, str(data["shipCid"]))
        self.set_name(row, data["title"], data["married"], data["marry_time"])
        self.set_id(row, data["id"], data["create_time"])
        self.set_class(row, data["type"])
        self.set_level(row, data["level"], data["exp"], data["nextExp"])

    def set_thumbnail(self, row, cid):
        ''' Column 0
        Set ship image (thumbnail) and categorize ships by cid along the way.
        '''
        assert (len(cid) == 8)

        if cid[-2:] == "11":
            self.ships_S.append(int(cid))
        elif cid[-2:] == "12":
            self.ships_M.append(int(cid))
        elif cid[-2:] == "13":
            self.ships_L.append(int(cid))
        else:
            err = "Unrecognized ship cid pattern: " + cid
            logging.warning(err)
            return None

        if cid[:3] == "100":
            prefix = "S_NORMAL_"
            self.non_mods.append(cid)
        elif cid[:3] == "110":
            prefix = "S_NORMAL_1"
            self.mods.append(cid)
        else:
            err = "Unrecognized ship cid pattern: " + cid
            logging.warning(err)
            return None

        img_path = "src/assets/S/" + prefix + str(int(cid[3:6])) + ".png"
        img = QPixmap()
        is_loaded =  img.load(get_data_path(img_path))
        if is_loaded:
            thumbnail = QTableWidgetItem()
            thumbnail.setData(Qt.DecorationRole, img.scaled(78, 44))
            self.setItem(row, 0, thumbnail)
        else:
            tmp = QPixmap()
            tmp.load(get_data_path("src/assets/S/0v0.png"))
            tmp2 = QTableWidgetItem()
            tmp2.setData(Qt.DecorationRole, tmp.scaled(78, 44))
            self.setItem(row, 0, tmp2)
            err = "Image path does not exist: " + img_path
            logging.warn(err)

    def set_name(self, *args):
        wig = QTableWidgetItem(args[1])
        if args[2] == 1:
            wig.setIcon(QIcon(get_data_path("src/assets/icons/ring_60.png")))
            s = "Married on " + self.hlp.ts_to_date(args[3])
            wig.setToolTip(s)
        self.setItem(args[0], 1, wig)

    def set_id(self, *args):
        wig = QTableWidgetItem(str(args[1]))
        s = "Met on " + self.hlp.ts_to_date(args[2])
        wig.setToolTip(s)
        self.setItem(args[0], 2, wig)

    def set_class(self, *args):
        wig = QTableWidgetItem(CONST.ship_type[args[1]])
        self.setItem(args[0], 3, wig)

    def set_level(self, *args):
        wig = QTableWidgetItem(str(args[1]))
        s = "Exp " + str(args[2]) + " / " + str(args[3])
        wig.setToolTip(s)
        self.setItem(args[0], 4, wig)

    def set_hp(self, *args):
        pass



# End of File