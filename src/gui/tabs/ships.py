import sys
import os
import logging
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QScrollArea, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QCheckBox, QTableView, QLineEdit
from PyQt5.QtCore import Qt, pyqtSlot, QSortFilterProxyModel, QVariant, QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon

from ...func import constants as CONST
from ...func.helper_function import Helper
from .ships_table import ShipTable, ShipTableDelegate
from .ships_top_checkbox import TopCheckboxes


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ShipSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.name_reg = None
        self.lock_opt = None
        # self.lock_opt = 'ALL'
        self.int_sort_cols = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.float_sort_cols = [15]
        self.no_sort_cols = [0]

    def setNameFilter(self, regex):
        '''
        reg = string, auto mapped to QString in Py3
        '''
        if isinstance(regex, str):
            regex = re.compile(regex)
        else:
            pass
        self.name_reg = regex
        self.invalidateFilter()

    def setLockFilter(self, is_lock):
        self.lock_opt = is_lock
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        '''
        overridden filterAcceptsRow(); virtual function
        return Boolean
        '''
        name_res = []
        if self.name_reg == None:
            name_res.append(source_row)
        else:
            name = ""
            name_col = 1
            name_index = self.sourceModel().index(source_row, name_col, source_parent)
            if name_index.isValid():
                name = self.sourceModel().data(name_index, Qt.DisplayRole)
                if name == None:
                    name = ""
                else:
                    pass
            else:
                pass
            # https://docs.python.org/3/library/re.html#re.compile
            name_res.append(self.name_reg.search(name))
        res = all(name_res)
        if res == False:
            return res
        else:
            pass

        lock_res = []
        if self.lock_opt == 'ALL':
            lock_res.append(source_row)
        else:
            lock_col = 2
            lock_index = self.sourceModel().index(source_row, lock_col, source_parent)
            if lock_index.isValid():
                lock = self.sourceModel().data(lock_index, Qt.DecorationRole)   # Detect if have ICON
                if self.lock_opt == 'YES':
                    lock_res.append(isinstance(lock, QIcon))
                elif self.lock_opt == 'NO':
                    lock_res.append(not isinstance(lock, QIcon))

        res = res and all(lock_res)
        return res

    def setFilterRegExp(self, string):
        return super().setFilterRegExp(string)

    def setFilterKeyColumn(self, column):
        return super().setFilterKeyColumn(column)

    def lessThan(self, source_left, source_right):
        self.headers = ["", "Name", "ID", "Class", "Lv.", "HP", "Torp.", "Eva.", "Range", "ASW", "AA", "Fire.", "Armor", "Luck", "LOS", "Speed", "Slot", "Equip.", "Tact."]
        
        if (source_left.isValid() and source_right.isValid):
            if (source_left.column() in self.no_sort_cols):
                # no sorting
                pass
            elif (source_left.column() in self.int_sort_cols):
                return int(source_left.data()) < int(source_right.data())
            elif (source_left.column() in self.float_sort_cols):
                return float(source_left.data()) < float(source_right.data())
        else:
            pass
        return super().lessThan(source_left, source_right)



class TabShips(QWidget):
    def __init__(self, realrun):
        super().__init__()
        self.hlp = Helper()

        scroll_box = QVBoxLayout(self)
        self.setLayout(scroll_box)
        scroll = QScrollArea(self)
        scroll_box.addWidget(scroll)
        scroll.setWidgetResizable(True)

        self.content_widget = QWidget(scroll)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setLayout(self.content_layout)
        scroll.setWidget(self.content_widget)

        self.upper_content_widget = QWidget(self.content_widget)
        self.lower_content_widget = QWidget(self.content_widget)

        self.content_layout.addWidget(self.upper_content_widget)
        self.content_layout.addWidget(self.lower_content_widget)
        self.content_layout.setStretch(0, 1)
        self.content_layout.setStretch(1, 10)


        self.table_view = QTableView(self.lower_content_widget)
        self.lower_layout = QGridLayout(self.lower_content_widget)
        self.lower_layout.addWidget(self.table_view, 1, 0, 1, 20)
        self.search_line       = QtWidgets.QLineEdit(self.lower_content_widget)
        self.lower_layout.addWidget(self.search_line, 0, 0, 1, 1)

        self.table_model = QStandardItemModel(self)

        self.ships = []
        for i in range(27):
            self.ships.append([])
        self.init_icons()

        self.table_proxy = ShipSortFilterProxyModel(self)
        self.table_proxy.setSourceModel(self.table_model)
        ck = TopCheckboxes(self.upper_content_widget, self.table_proxy)

        self.table_view.setModel(self.table_proxy)
        self.table_view.setItemDelegate(ShipTableDelegate(self.table_view))
        self.table_view.setSortingEnabled(True)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ships_S = []
        self.ships_M = []
        self.ships_L = []
        self.non_mods = []
        self.mods = []
        self.headers = ["", "Name", "ID", "Class", "Lv.", "HP", "Torp.", "Eva.", "Range", "ASW", "AA", "Fire.", "Armor", "Luck", "LOS", "Speed", "Slot", "Equip.", "Tact."]
        self.table_model.setColumnCount(len(self.headers))
        self.table_model.setHorizontalHeaderLabels(self.headers)

        self.search_line.textChanged.connect(self.table_proxy.setNameFilter)

        if realrun == 0:
            self.test()

    def test(self):
        logging.debug("Starting tests")
        import json
        p = get_data_path('api_getShipList.json')
        with open(p) as f:
            d = json.load(f)
        self.on_received_shiplist(d)

    @pyqtSlot(dict)
    def on_received_shiplist(self, data):
        if data == None:
            logging.error("Invalid ship list data.")
        else:
            # First sort by level, then sort by cid
            sorted_ships = sorted(data["userShipVO"], key=lambda x: (x['level'], x['shipCid']), reverse=True)
            for s in sorted_ships:
                self.ships[s["type"]].append(s)

            for ship_type, ship_lists in enumerate(self.ships):
                if (ship_type not in CONST.ship_type) and (len(ship_lists) != 0):
                    continue
                else:
                    for ship in ship_lists:
                        self.table_model.insertRow(self.table_model.rowCount())
                        self.add_ship(self.table_model.rowCount()-1, ship)


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
            self.table_model.setItem(row, 0, thumbnail)
        else:
            tmp = QPixmap()
            tmp.load(get_data_path("src/assets/S/0v0.png"))
            tmp2 = QStandardItem()
            tmp2.setData(QVariant(tmp.scaled(78, 44)), Qt.DecorationRole)
            self.table_model.setItem(row, 0, tmp2)
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
        self.table_model.setItem(args[0], 1, wig)

    def set_id(self, *args):
        wig = QStandardItem(str(args[1]))
        if args[2] == 1:
            wig.setIcon(self.lock_icon)
        else:
            # No icon for unlock as we uses QIcon/None to detect lock/unlock
            pass
        self.table_model.setItem(args[0], 2, wig)

    def set_class(self, *args):
        wig = QStandardItem(CONST.ship_type[args[1]])
        self.table_model.setItem(args[0], 3, wig)

    def set_level(self, *args):
        wig = QStandardItem(str(args[1]))

        if args[3] != -1:
            s = "Exp " + str(args[2]) + " / " + str(args[3])
            wig.setToolTip(s)
        else:
            pass
        self.table_model.setItem(args[0], 4, wig)


# End of File