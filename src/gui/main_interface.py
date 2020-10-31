import qdarkstyle

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThreadPool, QTimer

# GUI
from .side_dock import SideDock
from .main_interface_tabs import MainInterfaceTabs

# Functions
# from ..func.worker_thread import Worker
from ..func.helper_function import Helper

import logging
import json


class MainInterface(QMainWindow):
    # https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    sig_initGame = pyqtSignal(dict)
    sig_getShipList = pyqtSignal(dict)

    def __init__(self, server, channel, cookies, realrun=True):
        super().__init__()
        # self.qss = qss
        self.server = server
        self.channel = channel
        self.cookies = cookies
        self.realrun = realrun

        # self.sess = Session()
        self.hlp = Helper()

        # self.setStyleSheet(self.qss)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        user_w = QDesktopWidget().screenGeometry(-1).width()
        user_h = QDesktopWidget().screenGeometry(-1).height()
        self.resize(0.67*user_w, 0.67*user_h)

        layout = QHBoxLayout()
        self.bar = self.menuBar()
        self.add_file_menu()

        # # Multi-Threading
        self.threadpool = QThreadPool()
        logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        print(self.threadpool.activeThreadCount())


        # UI layout - top/L/R/bottom docks and central widget
        # https://doc.qt.io/archives/4.6/mainwindow.html
        self.table_widget = MainInterfaceTabs(self, self.threadpool, self.realrun)
        self.setCentralWidget(self.table_widget)

        self.side_dock_on = False
        self.init_side_dock()

        self.setLayout(layout)
        self.setWindowTitle('Warship Girls Viewer')

        if self.realrun:
            self._realrun()

    def _realrun(self):
        self.sig_initGame.connect(self.side_dock.on_received_resource)
        self.sig_initGame.connect(self.side_dock.on_received_name)
        self.sig_initGame.connect(self.side_dock.on_received_tasks)
        self.sig_initGame.connect(self.side_dock.on_received_lists)
        self.api_initGame()

        self.sig_getShipList.connect(self.table_widget.tab_ships.on_received_shiplist)
        self.api_getShipList()
        # self.pve_getPveData()
        # self.pve_getUserData()
        # self.pevent_getPveData()
        # self.bsea_getData()
        # self.live_getUserInfo()
        # self.six_getFleetInfo()
        # self.active_getUserData()
        # self.task_getAchievementList()
        # self.campaign_getUserData()

    @pyqtSlot()
    def on_dock_closed(self):
        self.side_dock_on = False

    def init_side_dock(self):
        if self.side_dock_on == False:
            self.side_dock = SideDock(self, self.realrun)
            self.addDockWidget(Qt.RightDockWidgetArea, self.side_dock)
            self.side_dock_on = True
        else:
            pass

    def open_author_info(self):
        def get_hyperlink(link, text):
            return "<a style=\"color:hotpink;text-align: center;\" href='"+link+"'>"+text+"</a>"

        msg = QMessageBox()
        # msg.setStyleSheet(self.qss)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.RichText)

        msg_str = '<h1>Warship Girls Viewer</h1>'
        msg_str += "\n"
        msg_str += get_hyperlink('https://github.com/WarshipGirls/WGViewer', 'GitHub - WGViewer')
        msg.setText(msg_str)
        msg.exec_()

    def add_file_menu(self):
        file_menu = self.bar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("save")
        file_menu.addAction("quit")

        view_menu = self.bar.addMenu("View")
        sidedock_action = QAction("&Open Navy Base Overview", self)
        sidedock_action.setShortcut("Ctrl+O")
        # sidedock_action.setStatusTip("...")
        sidedock_action.triggered.connect(self.init_side_dock)
        view_menu.addAction(sidedock_action)

        help_menu = self.bar.addMenu("Help")
        about_action = QAction("&About Warship Girls Viewer", self)
        about_action.triggered.connect(self.open_author_info)
        help_menu.addAction(about_action)


    # ================================
    # WGR APIs
    # ================================
    '''
    useful for dock
    userShipVO loop
      - lv, exp/nextExp, fleetId (fleed-belonging (0-8); don't need this, see initGame), equipment
      - id, tactics, title(name), type(shiptype)
      - love/loveMax, married
      - skillType, skillLevel, skillId,   (need mapping)
      - isLocked
      - capacitySlot/capacitySlotMax, missileSlot/missileSlotMax
      - equipmentArr?
      - battlePropsBasic, battleProps, battlePropsMax
          - hp, atk, def, torpedo, miss(evasion), antisub, speed, radar, range, luck
          - hit （命中？), airDef, cost
          - fuel, ammo, bauxite
    '''
    def api_getShipList(self):
        url = self.server + 'api/getShipList' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        if not self.realrun:
            with open('api_getShipList.json', 'w') as of:
                json.dump(data, of)
        self.sig_getShipList.emit(data)

    def api_initGame(self):
        url = self.server + 'api/initGame?&crazy=1' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        if not self.realrun:
            with open('api_initGame.json', 'w') as of:
                json.dump(data, of)
        self.sig_initGame.emit(data)

    def pve_getPveData(self):
        url = self.server + 'pve/getPveData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('pve_getPveData.json', 'w') as of:
            json.dump(data, of)

    def pevent_getPveData(self):
        url = self.server + 'pevent/getPveData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('pevent_getPveData.json', 'w') as of:
            json.dump(data, of)

    def bsea_getData(self):
        url = self.server + 'bsea/getData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('bsea_getData.json', 'w') as of:
            json.dump(data, of)

    def live_getUserInfo(self):
        url = self.server + 'live/getUserInfo' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('live_getUserInfo.json', 'w') as of:
            json.dump(data, of)

    # useless
    def six_getFleetInfo(self):
        url = self.server + 'six/getFleetInfo' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('six_getFleetInfo.json', 'w') as of:
            json.dump(data, of)

    def pve_getUserData(self):
        url = self.server + 'pve/getUserData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('pve_getUserData.json', 'w') as of:
            json.dump(data, of)

    def active_getUserData(self):
        url = self.server + 'active/getUserData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('active_getUserData.json', 'w') as of:
            json.dump(data, of)

    def task_getAchievementList(self):
        url = self.server + 'task/getAchievementList' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('task_getAchievementList.json', 'w') as of:
            json.dump(data, of)

    def campaign_getUserData(self):
        url = self.server + 'campaign/getUserData' + self.hlp.get_url_end(self.channel)
        raw_data = self.hlp.decompress_data(url=url, cookies=self.cookies)
        data = json.loads(raw_data)
        with open('campaign_getUserData.json', 'w') as of:
            json.dump(data, of)


# End of File