import sys
import os
import logging

from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea
from PyQt5.QtWidgets import QHeaderView, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot, QSize
# from PyQt5.QtGui import QSizePolicy

from ...func import constants as CONST


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QScrollArea):
    # https://pythonspot.com/pyqt5-table/
    def __init__(self, parent, realrun):
        super(QScrollArea, self).__init__(parent)
        # widget = QWidget()
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setAlignment(Qt.AlignTop)
        # https://stackoverflow.com/a/40139336


        # self.addWidget(scroll)

        self.ships = []
        self.tables = []
        # only 20 out of 27 is used by the game at 5.0.0
        for i in range(27):
            self.ships.append([])
            tb = QTableWidget()
            self.tables.append(tb)
            # self.main_layout.addWidget(tb)
        self.setLayout(self.main_layout)

        if realrun == False:
            self.test()

    def test(self):
        logging.debug("Starting tests")
        import json
        p = get_data_path('api_getShipList.json')
        with open(p) as f:
            d = json.load(f)
        self.on_received_shiplist(d)

    # def init_table(self,):
    #     list_box = QVBoxLayout(self)
    #     self.setLayout(list_box)

    #     scroll = QScrollArea(self)
    #     list_box.addWidget(scroll)
    #     scroll.setWidgetResizable(True)
    #     scroll_content = QWidget(scroll)

    #     scroll_layout = QVBoxLayout(scroll_content)
    #     scroll_content.setLayout(scroll_layout)

    def get_table_size(self, t):
        logging.debug(t.verticalHeader().width())
        logging.debug(t.columnCount())
        logging.debug(t.verticalHeader().height())
        logging.debug(t.rowCount())
        w = t.verticalHeader().width() + 4
        for i in range(t.columnCount()):
            w += t.columnWidth(i)
        h = t.horizontalHeader().height() + 4
        for i in range(t.rowCount()):
            h += t.rowHeight(i)
        print(w, h)
        return QSize(w, h)

    def init_table(self, table):
        table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        table.resizeColumnsToContents()
        table.setFixedSize(table.horizontalHeader().length() + 
                           table.verticalHeader().width(),
                           table.verticalHeader().length() + 
                           table.horizontalHeader().height())

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