import json
import logging
import os
import qdarkstyle

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThreadPool, QTimer
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import QAction

# GUI
from .side_dock import SideDock
from .main_interface_tabs import MainInterfaceTabs

# Functions
# from ..func.worker_thread import Worker
from ..func import data as wgr_data
from ..func.wgr_api import WGR_API
from ..func.helper_function import Helper


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

        self.hlp = Helper()
        self.api = WGR_API(self.server, self.channel, self.cookies)

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
        self.table_widget = MainInterfaceTabs(self, self.api, self.threadpool, self.realrun)
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
        msg.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
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