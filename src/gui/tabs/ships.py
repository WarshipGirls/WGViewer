import sys
import os
import logging
import traceback

from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QComboBox, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QHeaderView, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtGui import QPixmap

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
        self.layout.setContentsMargins(0,0,0,0)

        for i in range(10):
            self.layout.setColumnStretch(i, 1)
        self.init_dropdowns()
        self.init_ship_boxes()

    def init_dropdowns(self):
        lock_select = ["ALL", "YES", "NO"]
        self.add_dropdown("LOCK", lock_select, self.lock_handler, 0, 0)
        level_select = ["ALL", "Lv. 1", "> Lv. 1", "\u2265 Lv. 90", "\u2265 Lv. 100", "= Lv. 110"]
        self.add_dropdown("LEVEL", level_select, self.level_handler, 0, 1)
        value_select = ["Equip. Incl.", "Raw Value"]
        self.add_dropdown("VALUE", value_select, self.value_handler, 0, 2)
        mod_select = ["ALL", "Non-mod. Only", "Mod I. Only"]
        self.add_dropdown("MOD.", mod_select, self.mod_handler, 0, 3)
        rarity_select = ["\u2606 1", "\u2606 2", "\u2606 3", "\u2606 4", "\u2606 5", "\u2606 6"]
        self.add_dropdown("RARITY", rarity_select, self.rarity_handler, 0, 4)
        # current = 30/60, max only = 60
        health_select = ["Current Value", "Max Only"]
        self.add_dropdown("HEALTH", health_select, self.health_handler, 0, 5)
        married_select = ["ALL", "Married Only", "Non Married Only"]
        self.add_dropdown("MARRY", married_select, self.marry_handler, 0, 6)

    def add_dropdown(self, label, choices, handler, x, y):
        w = QWidget()
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
        self.layout.addWidget(w, x, y, 1, 1)

    def lock_handler(self, text):
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
            self.layout.addWidget(b, 1, k, 1, 1)
            # https://stackoverflow.com/a/35821092
            self.first_boxes[k].stateChanged.connect(lambda _, b=self.first_boxes[k]: self.checkbox_handler(b))
        self.second_boxes = []
        for k, v in enumerate(second_row_types):
            b = QCheckBox(v, self)
            self.second_boxes.append(b)
            self.layout.addWidget(b, 2, k, 1, 1)
            self.second_boxes[k].stateChanged.connect(lambda _, b=self.second_boxes[k]: self.checkbox_handler(b))

    def checkbox_handler(self, cb):
        if cb.isChecked():
            print("checked " + cb.text())
        else:
            print("unchecked " + cb.text())

class ShipTable(QTableWidget):
    def __init__(self, rows):
        super().__init__()
        self.setStyleSheet("")
        self.headers = ["", "Name", "ID", "Class", "Lv.", "HP", "Torp.", "Eva.", "Range", "ASW", "AA", "Fire.", "Armor", "Luck", "LOS", "Speed", "Slot", "Equip.", "Tact."]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setShowGrid(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        try:
            for i in range(rows):
                self.insertRow(i)
                # QPixmap vs. QImage https://stackoverflow.com/a/10315773
                path = "src/assets/S/S_NORMAL_1.png"    # wxh=363x88, cropped=156x88
                img = QPixmap()
                is_loaded = img.load(path)
                if is_loaded:
                    self.setRowHeight(i, 50)
                    self.setColumnWidth(i, 80)
                    thumbnail = QTableWidgetItem()
                    thumbnail.setData(Qt.DecorationRole, img.scaled(78, 44))
                    self.setItem(i, 0, thumbnail)
                else:
                    print(path)

            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setMaximumSize(self.getQTableWidgetSize())
            self.setMinimumSize(self.getQTableWidgetSize())
            self.show()
        except Exception as e:
            print(traceback.format_exc())

    def getQTableWidgetSize(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

class TabShips(QWidget):
    def __init__(self, realrun):
        # super(QWidget, self).__init__(parent)
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
        self.show()

        self.ships = []
        self.tables = []
        # only 20 out of 27 is used by the game at 5.0.0
        for i in range(27):
            self.ships.append([])
            tb = QTableWidget()
            self.tables.append(tb)

        if realrun == False:
            self.test()

    def test(self):
        logging.debug("Starting tests")
        x = ShipTable(50)
        y = ShipTable(50)
        ck = TopCheckboxes()
        self.scroll_layout.addWidget(ck)
        self.scroll_layout.addWidget(x)
        self.scroll_layout.addWidget(y)

    # def init_table(self, table):
    #     table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    #     table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #     table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    #     table.resizeColumnsToContents()
    #     table.setFixedSize(table.horizontalHeader().length() + 
    #                        table.verticalHeader().width(),
    #                        table.verticalHeader().length() + 
    #                        table.horizontalHeader().height())

    @pyqtSlot(dict)
    def on_received_shiplist(self, data):
        if data != None:
            for s in data["userShipVO"]:
                self.ships[s["type"]].append(s)
            for ship_type, ship_lists in enumerate(self.ships):
                if ship_type not in CONST.ship_type:
                    pass
                else:
                    if len(ship_lists) != 0 and ship_type==12:
                        tb = self.tables[ship_type]
                        self.main_layout.addWidget(tb)
                        print(ship_type, len(ship_lists))
                        row = col = 0
                        tb.setColumnCount(1)    # TODO: set count according to ship type
                        # self.tables[ship_type].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                        for ship in ship_lists:
                            tb.insertRow(row)
                            tb.setItem(row, col, QTableWidgetItem(ship["title"]))
                            row += 1
                        # self.init_table(self.tables[ship_type])
                        # self.tables[ship_type].resize(0,0)
                        # tb.setHorizontalHeaderLabels(self.hheaders)
                        tb.verticalHeader().setVisible(False)
                        tb.resizeRowsToContents()
                        tb.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                        tb.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                        tb.setMaximumSize(self.get_table_size(tb))
                        tb.setMinimumSize(self.get_table_size(tb))
                '''
                title = u["title"]
                cid = u["shipCid"]
                lv = u["level"]
                # lv hover
                exp = u["exp"]
                n_exp = u["nextExp"]
                # name hover
                love = u["love"]
                love_max = u["loveMax"]
                equips = u["equipment"]
                _id = u["id"]
                tact = u["tactics"]
                is_locked = u["isLocked"]
                # if all 0, skip
                cap_slot = u["capacitySlot"]
                cap_max = u["capacitySlotMax"]
                ms_slot = u["missileSlot"]
                ms_max = u["missileSlotMax"]
                # w/o equip
                sn = u["battlePropsBasic"]
                # with equip but wounded
                sp = u["battleProps"]
                # with equip and full HP/full refuel etc
                sm = u["battlePropsMax"]   
                try:         
                    skill = u["skillType"] #str
                    skill_lv = u["skillLevel"]
                except KeyError:
                    # This ship doesn't have skill
                    pass
                '''



# End of File