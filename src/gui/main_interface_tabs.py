import sys
import os

from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout,QGridLayout
from PyQt5.QtCore import QTimer, pyqtSlot

from .tabs.advance_functions import TabAdvanceFunctions
from .tabs.ships import TabShips


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class MainInterfaceTabs(QWidget):
    ''' Tentative plans
        Tab 1 = Sortie
        Tab 2 = 1-8 Fleets
        Tab 3 = All Ships
        Tab 4 = All Equips
        Tab 5 = All tactics
        Tab n = Extra functions
    '''
    def __init__(self, parent, threadpool, realrun):
        super(QWidget, self).__init__(parent)
        self.realrun = realrun
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.tab_ships = TabShips(self.realrun)
        label2 = QLabel("test")
        tabwidget = QTabWidget()
        tabwidget.addTab(self.tab_ships, "  Ship  ")
        tabwidget.addTab(label2, "  Tab2  ")
        self.layout.addWidget(tabwidget, 0, 0)
        # self.threadpool = threadpool
        # self.realrun = realrun

        # self.main_layout = QVBoxLayout(self)
        # self.setLayout(self.main_layout)
        # # self.resize(1000, 1)    # TODO: this seems not working

        # self.init_tab_bar()
        
        # # Create first tab
        # self.tab1.layout = QVBoxLayout(self)
        # self.pushButton1 = QPushButton("PyQt5 button")

        # self.l = QLabel("Start")
        # self.counter = 0
        # self.timer = QTimer()
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.recurring_timer)
        # self.timer.start()

        # self.tab1.layout.addWidget(self.pushButton1)
        # self.tab1.layout.addWidget(self.l)
        # self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        # self.main_layout.addWidget(self.tabs)

        if self.realrun == False:
            self.test()

    def test(self):
        pass
        # import json
        # p = get_data_path('api_getShipList.json')
        # with open(p) as f:
        #     d = json.load(f)
        # self.on_received_shiplist(d)

    def init_tab_bar(self):
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab_ships = TabShips(self, self.realrun)
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab_advance = TabAdvanceFunctions(self)

        # Add tabs
        self.tabs.addTab(self.tab_ships,"  Ships  ")
        self.tabs.addTab(self.tab1,"  Sortie  ")
        self.tabs.addTab(self.tab2,"  Fleets  ")
        self.tabs.addTab(self.tab4,"  Equipment  ")
        self.tabs.addTab(self.tab5,"  Tactics  ")
        self.tabs.addTab(self.tab_advance,"  Advance Functions  ")

    def recurring_timer(self):
        self.counter +=1
        print("I'm in " + os.path.basename(__file__))
        print("active thread = " + str(self.threadpool.activeThreadCount()))
        self.l.setText("Counter: %d" % self.counter)


# End of File