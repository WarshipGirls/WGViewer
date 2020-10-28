import sys
import os

from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, pyqtSlot

from .tab_advance_functions import TabAdvanceFunctions


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class MainInterfaceTabs(QWidget):
    def __init__(self, parent, threadpool, realrun):
        super(QWidget, self).__init__(parent)
        self.threadpool = threadpool

        self.main_layout = QVBoxLayout(self)
        self.resize(1000, 1)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        # self.tab1 = QWidget()
        self.tab1 = TabAdvanceFunctions(self)
        self.tab2 = QWidget()
        self.tabs.resize(30,20)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")

        self.l = QLabel("Start")
        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.layout.addWidget(self.l)
        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

        # List created by ship-type number from 1-18
        # CV, CVL, AV, BB, BBV
        # BC, CA, CAV, CLT, CL
        # BM, DD, SSV, SS, SC
        # AP, ASDG, AADG
        self.ships = []
        for i in range(18):
            self.ships.append([])

        if realrun == False:
            self.test()

    def test(self):
        import json
        p = get_data_path('api_getShipList.json')
        with open(p) as f:
            d = json.load(f)
        self.on_received_shiplist(d)

    def recurring_timer(self):
        self.counter +=1
        print("I'm in " + os.path.basename(__file__))
        print("active thread = " + str(self.threadpool.activeThreadCount()))
        self.l.setText("Counter: %d" % self.counter)



    @pyqtSlot(dict)
    def on_received_shiplist(self, data):
        if data != None:
            x = data["userShipVO"]
            for u in x: 
                title = u["title"]
                ship_type = u["type"]
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
                # naked
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


# End of File