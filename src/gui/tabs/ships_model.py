import sys
import os
import logging

from PyQt5.QtCore import Qt, QVariant, pyqtSlot, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon

from . import ships_constant as SCONST
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
        # NOTE: `data()` is a method of `QStandardItemModel()`
        self.hlp = Helper()

        self.ships_S = []
        self.ships_M = []
        self.ships_L = []
        self.non_mods = []
        self.mods = []
        self.ships_raw_data = None

        self.value_opt = SCONST.value_select[0]

        self.headers = SCONST._header
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.init_icons()

    def init_icons(self):
        # To avoid repeatedly loading same icon, preload them
        self.ring_icon = QIcon(get_data_path("src/assets/icons/ring_60.png"))
        self.lock_icon = QIcon(get_data_path("src/assets/icons/lock_64.png"))

    def set_data(self, _data):
        self.ships_raw_data = _data

        self.ships_data = []
        for i in range(27):
            self.ships_data.append([])
        for s in self.ships_raw_data:
            self.ships_data[s["type"]].append(s)
        for ship_type, ship_lists in enumerate(self.ships_data):
            if (ship_type not in CONST.ship_type) and (len(ship_lists) != 0):
                continue
            else:
                for ship in ship_lists:
                    self.insertRow(self.rowCount())
                    self.add_ship(self.rowCount()-1, ship)

    def add_ship(self, row, d):
        self.set_thumbnail(row, str(d["shipCid"]))
        self.set_name(row, d["title"], d["married"], d["create_time"], d["marry_time"])
        self.set_id(row, d["id"], d["isLocked"])
        self.set_class(row, d["type"])
        self.set_level(row, d["level"], d["exp"], d["nextExp"])

        # self.set_stats(row, d["battleProps"], , d["battlePropsBasic"])
        self.set_stats(row, d["battleProps"], d["battlePropsMax"])

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

    @pyqtSlot(str)
    def on_stats_changed(self, *args):
        '''
        Getting check box update signal
        '''
        if args[0] in SCONST.value_select:
            self.value_opt = args[0]
        else:
            pass

        self.update_stats()

    def update_stats(self, *args):
        for row in range(self.rowCount()):
            _id_idx = self.index(row, 2, QModelIndex())
            _id = int(self.data(_id_idx, Qt.DisplayRole))
            _ship = next(i for i in self.ships_raw_data if i['id'] == _id)

            if self.value_opt == SCONST.value_select[0]:    # curr
                s = str(_ship['battleProps']['hp']) + "/" + str(_ship['battlePropsMax']['hp'])
                self.item(row, 5).setData(_ship['battleProps']['hp'], Qt.DisplayRole)
                self.item(row, 6).setData(_ship['battleProps']['torpedo'], Qt.DisplayRole)
                self.item(row, 7).setData(_ship['battleProps']['miss'], Qt.DisplayRole)
                self.item(row, 8).setData(CONST.range_type[_ship['battleProps']['range']], Qt.DisplayRole)
                self.item(row, 9).setData(_ship['battleProps']['antisub'], Qt.DisplayRole)
                self.item(row, 10).setData(_ship['battleProps']['airDef'], Qt.DisplayRole)
                self.item(row, 11).setData(_ship['battleProps']['atk'], Qt.DisplayRole)
                self.item(row, 12).setData(_ship['battleProps']['def'], Qt.DisplayRole)
                self.item(row, 13).setData(_ship['battleProps']['luck'], Qt.DisplayRole)
                self.item(row, 14).setData(_ship['battleProps']['radar'], Qt.DisplayRole)
                self.item(row, 15).setData(_ship['battleProps']['speed'], Qt.DisplayRole)
            elif self.value_opt == SCONST.value_select[1]:  # max
                self.item(row, 5).setData(_ship['battlePropsMax']['hp'], Qt.DisplayRole)
                self.item(row, 6).setData(_ship['battlePropsMax']['torpedo'], Qt.DisplayRole)
                self.item(row, 7).setData(_ship['battlePropsMax']['miss'], Qt.DisplayRole)
                self.item(row, 9).setData(_ship['battlePropsMax']['antisub'], Qt.DisplayRole)
                self.item(row, 11).setData(_ship['battlePropsMax']['atk'], Qt.DisplayRole)
                self.item(row, 12).setData(_ship['battlePropsMax']['def'], Qt.DisplayRole)
                self.item(row, 13).setData(_ship['battlePropsMax']['luck'], Qt.DisplayRole)
                self.item(row, 14).setData(_ship['battlePropsMax']['radar'], Qt.DisplayRole)
            elif self.value_opt == SCONST.value_select[2]:  # raw
                self.item(row, 5).setData(_ship['battlePropsBasic']['hp'], Qt.DisplayRole)
                self.item(row, 6).setData(_ship['battlePropsBasic']['torpedo'], Qt.DisplayRole)
                self.item(row, 7).setData(_ship['battlePropsBasic']['miss'], Qt.DisplayRole)
                self.item(row, 8).setData(CONST.range_type[_ship['battlePropsBasic']['range']], Qt.DisplayRole)
                self.item(row, 9).setData(_ship['battlePropsBasic']['antisub'], Qt.DisplayRole)
                self.item(row, 10).setData(_ship['battlePropsBasic']['airDef'], Qt.DisplayRole)
                self.item(row, 11).setData(_ship['battlePropsBasic']['atk'], Qt.DisplayRole)
                self.item(row, 12).setData(_ship['battlePropsBasic']['def'], Qt.DisplayRole)
                self.item(row, 13).setData(_ship['battlePropsBasic']['luck'], Qt.DisplayRole)
                self.item(row, 14).setData(_ship['battlePropsBasic']['radar'], Qt.DisplayRole)
                self.item(row, 15).setData(_ship['battlePropsBasic']['speed'], Qt.DisplayRole)
            else:
                pass
    # "Torp.", "Eva.", "Range", "ASW", "AA", "Fire.", "Armor", "Luck", "LOS", "Speed", "Slot", "Equip.", "Tact."]
    def set_stats(self, *args):
        # set current ship stats as default
        
        # Design thinking: I thought set eye-catching color for not-full hp. 
        # but there will be dock in the future, so it is redundant to set color here
        # also extra work of set/reset-ing color
        s = str(args[1]['hp']) + "/" + str(args[2]['hp'])
        wig = QStandardItem(s)
        self.setItem(args[0], 5, wig)

        self.setItem(args[0], 6, QStandardItem(str(args[1]['torpedo'])))
        self.setItem(args[0], 7, QStandardItem(str(args[1]['miss'])))
        self.setItem(args[0], 8, QStandardItem(CONST.range_type[args[1]['range']]))
        self.setItem(args[0], 9, QStandardItem(str(args[1]['antisub'])))
        self.setItem(args[0], 10, QStandardItem(str(args[1]['airDef'])))
        self.setItem(args[0], 11, QStandardItem(str(args[1]['atk'])))
        self.setItem(args[0], 12, QStandardItem(str(args[1]['def'])))
        self.setItem(args[0], 13, QStandardItem(str(args[1]['luck'])))
        self.setItem(args[0], 14, QStandardItem(str(args[1]['radar'])))
        self.setItem(args[0], 15, QStandardItem(str(args[1]['speed'])))



# End of File