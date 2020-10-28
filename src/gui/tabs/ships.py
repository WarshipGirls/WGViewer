import sys
import os
import logging

from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import pyqtSlot

from ...func import constants as CONST


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QWidget):
    def __init__(self, parent, realrun):
        super(QWidget, self).__init__(parent)
        # https://stackoverflow.com/a/40139336
        # self.widgetResizable(True)
        self.main_layout = QVBoxLayout()

        self.ships = []
        self.tables = []
        # only 20 out of 27 is used by the game at 5.0.0
        for i in range(27):
            self.ships.append([])
            self.tables.append(QTableWidget())

        if realrun == False:
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
        if data != None:
            for s in data["userShipVO"]:
                self.ships[s["type"]].append(s)
            for ship_type, ship_lists in enumerate(self.ships):
                if ship_type not in CONST.ship_type:
                    pass
                else:
                    if len(ship_lists) != 0:
                        self.main_layout.addWidget(self.tables[ship_type])
                        print(ship_type, len(ship_lists))
                        row = col = 0
                        self.tables[ship_type].setColumnCount(1)
                        for ship in ship_lists:
                            self.tables[ship_type].insertRow(row)
                            self.tables[ship_type].setItem(row, col, QTableWidgetItem(ship["title"]))
                            row += 1
                self.setLayout(self.main_layout)
                '''
                title = u["title"]
                cid = u["shipCid"]
                lv = u["level"]
                exp = u["exp"]
                n_exp = u["nextExp"]
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