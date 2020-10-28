import sys
import os
import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QWidget):
    def __init__(self, parent, realrun):
        super(QWidget, self).__init__(parent)


        self.ships = []
        # only 20 out of 27 is used by the game at 5.0.0
        for i in range(27):
            self.ships.append([])

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
            x = data["userShipVO"]
            for s in x:
                self.ships[s["type"]].append(s)
            for i in range(len(self.ships)):
                print(i, len(self.ships[i]))
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