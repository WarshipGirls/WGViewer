import json
import logging
import os
import qdarkstyle

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThreadPool, QTimer, QSettings
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout
from PyQt5.QtWidgets import QDesktopWidget

# GUI
from .side_dock import SideDock
from .main_interface_tabs import MainInterfaceTabs

# Functions
# from ..func.worker_thread import Worker
from .main_interface_menubar import MainInterfaceMenuBar
from ..data import data as wgr_data
from ..func.wgr_api import WGR_API


class MainInterface(QMainWindow):
    # https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    sig_initGame = pyqtSignal(dict)
    sig_getShipList = pyqtSignal(dict)

    def __init__(self, server, channel, cookies, realrun=True):
        super().__init__()
        self.server = server
        self.channel = channel
        self.cookies = cookies
        self.realrun = realrun
        self.side_dock_on = False

        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)
        self.threadpool = QThreadPool()
        self.api = WGR_API(self.server, self.channel, self.cookies)
        self.setMenuBar(MainInterfaceMenuBar(self))

        self.init_data_files()
        self.init_ui()

        if self.qsettings.contains("UI/init_side_dock"):
            if self.qsettings.value("UI/init_side_dock") == "true":
                pass
            else:
                self.init_side_dock()
        else:
            self.qsettings.setValue("UI/init_side_dock", False)
            self.init_side_dock()

        # # Multi-Threading TODO?
        logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        print(self.threadpool.activeThreadCount())

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


    # ================================
    # Initialization
    # ================================

    def set_color_scheme(self):
        # style should be set at Login Form, following one-liner is kept while by-passing Login
        s = self.qsettings.value("style") if self.qsettings.contains("style") else "qdarkstyle"
        if s == "native":
            self.setStyleSheet("")
        else:
            self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            self.qsettings.setValue("style", "qdarkstyle")

    def init_ui(self):
        self.set_color_scheme()
        user_w = QDesktopWidget().screenGeometry(-1).width()
        user_h = QDesktopWidget().screenGeometry(-1).height()
        self.resize(0.67*user_w, 0.67*user_h)

        # UI layout - top/L/R/bottom docks and central widget
        # https://doc.qt.io/archives/4.6/mainwindow.html
        self.table_widget = MainInterfaceTabs(self, self.api, self.threadpool, self.realrun)
        self.setCentralWidget(self.table_widget)

        self.setLayout(QHBoxLayout())
        self.setWindowTitle('Warship Girls Viewer')

    def init_side_dock(self):
        if self.side_dock_on == False:
            self.side_dock = SideDock(self, self.realrun)
            self.addDockWidget(Qt.RightDockWidgetArea, self.side_dock)
            self.side_dock_on = True
        else:
            pass

    def init_data_files(self):
        num = len(os.listdir(wgr_data.get_init_dir()))
        # As of 5.0.0, there should be 30 files
        if num != 30:
            wgr_data.save_init_data()
        else:
            pass


    # ================================
    # Events
    # ================================


    @pyqtSlot()
    def on_dock_closed(self):
        self.side_dock_on = False


    # ================================
    # WGR APIs
    # ================================


    def api_getShipList(self):
        data = self.api.api_getShipList()
        with open('api_getShipList.json', 'w') as of:
            json.dump(data, of)
        self.sig_getShipList.emit(data)

    def api_initGame(self):
        data = self.api.api_initGame()
        with open('api_initGame.json', 'w') as of:
            json.dump(data, of)
        self.sig_initGame.emit(data)

        # save necessary data
        user_dir = wgr_data.get_user_dir()
        with open(os.path.join(user_dir, 'equipmentVo.json'), 'w') as f:
            json.dump(data['equipmentVo'], f, ensure_ascii=False, indent=4)

        with open(os.path.join(user_dir, 'tactics.json'), 'w') as f:
            json.dump(data['tactics'], f, ensure_ascii=False, indent=4)


# End of File