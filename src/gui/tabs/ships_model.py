import sys
import os
import logging

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon

from ...func import constants as CONST
from ...func.helper_function import Helper

def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ShipModel(QStandardItemModel):
    def __init__(self, *args, **kwargs):
        QStandardItemModel.__init__(self, *args, **kwargs)
        self.hlp = Helper()

        self.ships_S = []
        self.ships_M = []
        self.ships_L = []
        self.non_mods = []
        self.mods = []
        self.headers = ["", "Name", "ID", "Class", "Lv.", "HP", "Torp.", "Eva.", "Range", "ASW", "AA", "Fire.", "Armor", "Luck", "LOS", "Speed", "Slot", "Equip.", "Tact."]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.init_icons()

    def init_icons(self):
        # To avoid repeatedly loading same icon, preload them
        self.ring_icon = QIcon(get_data_path("src/assets/icons/ring_60.png"))
        self.lock_icon = QIcon(get_data_path("src/assets/icons/lock_64.png"))

    def add_ship(self, row, data):
        self.set_thumbnail(row, str(data["shipCid"]))
        self.set_name(row, data["title"], data["married"], data["create_time"], data["marry_time"])
        self.set_id(row, data["id"], data["isLocked"])
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

        # QTableWidgetItem requires unique assignment; thus, same pic cannot assign twice. Differ from QIcon
        img_path = "src/assets/S/" + prefix + str(int(cid[3:6])) + ".png"
        img = QPixmap()
        is_loaded =  img.load(get_data_path(img_path))
        if is_loaded:
            thumbnail = QStandardItem()
            thumbnail.setData(QVariant(img.scaled(78, 44)), Qt.DecorationRole)
            self.setItem(row, 0, thumbnail)
        else:
            tmp = QPixmap()
            tmp.load(get_data_path("src/assets/S/0v0.png"))
            tmp2 = QStandardItem()
            tmp2.setData(QVariant(tmp.scaled(78, 44)), Qt.DecorationRole)
            self.setItem(row, 0, tmp2)
            err = "Image path does not exist: " + img_path
            logging.warn(err)

    def set_name(self, *args):
        wig = QStandardItem(args[1])
        s = "Met on " + self.hlp.ts_to_date(args[3])
        if args[2] == 1:
            wig.setIcon(self.ring_icon)
            s += "\nMarried on " + self.hlp.ts_to_date(args[4])
        else:
            pass
        wig.setToolTip(s)
        self.setItem(args[0], 1, wig)

    def set_id(self, *args):
        wig = QStandardItem(str(args[1]))
        if args[2] == 1:
            wig.setIcon(self.lock_icon)
        else:
            # No icon for unlock as we uses QIcon/None to detect lock/unlock
            pass
        self.setItem(args[0], 2, wig)

    def set_class(self, *args):
        wig = QStandardItem(CONST.ship_type[args[1]])
        self.setItem(args[0], 3, wig)

    def set_level(self, *args):
        wig = QStandardItem(str(args[1]))

        if args[3] != -1:
            s = "Exp " + str(args[2]) + " / " + str(args[3])
            wig.setToolTip(s)
        else:
            pass
        self.setItem(args[0], 4, wig)


# End of File