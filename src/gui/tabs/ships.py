import sys
import os
import logging
import traceback

from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QComboBox, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QHeaderView, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtGui import QPixmap, QIcon

from ...func import constants as CONST


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TopCheckboxes(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        # self.layout.setContentsMargins(0,0,0,0)
        # TODO: fix the size
        # self.setGeometry(0,0, 500, 100)
        # self.resize(200, 200)

        for i in range(10):
            self.layout.setColumnStretch(i, 1)
        self.init_dropdowns()
        self.init_ship_boxes()
        # self.layout.setRowMinimumHeight(0, 0)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)
        # self.setFixedHeight(100)
        # self.setFixedWidth(1000)  # not working as expected
        print(self.width(), self.height())

    def init_dropdowns(self):
        lock_select = ["ALL", "YES", "NO"]
        level_select = ["ALL", "Lv. 1", "> Lv. 1", "\u2265 Lv. 90", "\u2265 Lv. 100", "= Lv. 110"]
        value_select = ["Equip. Incl.", "Raw Value"]
        mod_select = ["ALL", "Non-mod. Only", "Mod I. Only"]
        health_select = ["Current Value", "Max Only"]
        rarity_select = ["\u2606 1", "\u2606 2", "\u2606 3", "\u2606 4", "\u2606 5", "\u2606 6"]
        married_select = ["ALL", "Married Only", "Non Married Only"]
        size_select = ["ALL", "SMALL", "MIDIUM", "LARGE"]
        self.add_dropdown("LOCK", lock_select, self.lock_handler, 0, 0)
        self.add_dropdown("LEVEL", level_select, self.level_handler, 0, 1)
        self.add_dropdown("VALUE", value_select, self.value_handler, 0, 2)
        self.add_dropdown("MOD.", mod_select, self.mod_handler, 0, 3)
        self.add_dropdown("Type (Size)", size_select, self.size_handler, 0, 4)
        self.add_dropdown("RARITY", rarity_select, self.rarity_handler, 0, 5)
        # current = 30/60, max only = 60
        self.add_dropdown("HEALTH", health_select, self.health_handler, 0, 6)
        self.add_dropdown("MARRY", married_select, self.marry_handler, 0, 7)

    def add_dropdown(self, label, choices, handler, x, y):
        w = QWidget()
        w.setFixedHeight(40)
        # w.setFixedWidth(200)  # not working as expected
        wl = QHBoxLayout()
        w.setLayout(wl)
        l = QLabel(label)
        lc = QComboBox()
        lc.addItems(choices)
        lc.currentTextChanged.connect(handler)
        wl.addWidget(l)
        wl.addWidget(lc)
        wl.setStretch(0, 2)
        wl.setStretch(1, 8)
        # self.layout.addWidget(w, x, y, 1, 1)
        print("dropdown")
        print(w.width(), w.height())
        self.layout.addWidget(w, x, y)

    def lock_handler(self, text):
        print(text)

    def size_handler(self, text):
        print(text)

    def level_handler(self, text):
        print(text)

    def value_handler(self, text):
        print(text)

    def mod_handler(self, text):
        print(text)

    def rarity_handler(self, text):
        print(text)

    def health_handler(self, text):
        print(text)

    def marry_handler(self, text):
        print(text)

    def init_ship_boxes(self):
        # in the ascending order of ship types (int)
        first_row_types = ["CV", "CVL", "AV", "BB", "BBV", "BC", "CA", "CAV", "CLT", "CL"]
        second_row_types = ["BM", "DD", "SSV", "SS", "SC", "AP", "ASDG", "AADG", "CB", "BBG"]

        self.first_boxes = []
        for k, v in enumerate(first_row_types):
            b = QCheckBox(v, self)
            self.first_boxes.append(b)
            # self.layout.addWidget(b, 1, k, 1, 1)
            self.layout.addWidget(b, 1, k)
            # https://stackoverflow.com/a/35821092
            self.first_boxes[k].stateChanged.connect(lambda _, b=self.first_boxes[k]: self.checkbox_handler(b))
        self.second_boxes = []
        for k, v in enumerate(second_row_types):
            b = QCheckBox(v, self)
            self.second_boxes.append(b)
            # self.layout.addWidget(b, 2, k, 1, 1)
            self.layout.addWidget(b, 2, k)
            self.second_boxes[k].stateChanged.connect(lambda _, b=self.second_boxes[k]: self.checkbox_handler(b))

    def checkbox_handler(self, cb):
        if cb.isChecked():
            print("checked " + cb.text())
        else:
            print("unchecked " + cb.text())

class ShipTable(QTableWidget):
    def __init__(self):
        super().__init__()
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

    def adjust_table_size(self):
        self.setMaximumSize(self.get_table_widget_size())
        self.setMinimumSize(self.get_table_widget_size())

        i = "table w = " + str(self.width()) + ", h = " + str(self.height())
        logging.debug(i)    # 1904, 2367

    def add_ship(self, row, data):
        self.set_thumbnail(row, data)
        self.set_name(row, data)

    def set_name(self, row, data):
        n = data["title"]
        n_wig = QTableWidgetItem(n)
        if data["married"] == 1:
            n_wig.setIcon(QIcon(get_data_path("src/assets/icons/ring_60.png")))
        self.setItem(row, 1, n_wig)

    def set_thumbnail(self, row, data):
        '''
        Set ship image (thumbnail) and categorize cid along the way.
        '''
        cid = str(data["shipCid"])
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

    def get_table_widget_size(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

class TabShips(QWidget):
    def __init__(self, realrun):
        super().__init__()

        list_box = QVBoxLayout(self)
        self.setLayout(list_box)

        scroll = QScrollArea(self)
        list_box.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)

        self.scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(self.scroll_layout)
        scroll.setWidget(scroll_content)

        # only 20 out of 27 is used by the game at 5.0.0
        # self.ships = [[]] * 27    # this binds to same list
        self.ships = []
        for i in range(27):
            self.ships.append([])
        ck = TopCheckboxes()
        self.scroll_layout.addWidget(ck)
        # TODO? https://github.com/WarshipGirls/WGViewer/issues/7
        self.ship_table = ShipTable()
        self.scroll_layout.addWidget(self.ship_table)

        if realrun == 0:
            self.test()
        print("tabships")
        # self.setFixedHeight(200)
        print(self.width(), self.height())

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
            for s in data["userShipVO"]:
                self.ships[s["type"]].append(s)

            for ship_type, ship_lists in enumerate(self.ships):
                if (ship_type not in CONST.ship_type) and (len(ship_lists) != 0):
                    continue
                else:
                    for ship in ship_lists:
                        self.ship_table.insertRow(self.ship_table.rowCount())
                        self.ship_table.add_ship(self.ship_table.rowCount()-1, ship)
            self.ship_table.adjust_table_size()


# End of File