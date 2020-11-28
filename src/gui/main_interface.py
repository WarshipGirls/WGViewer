import json
import logging
import os
import qdarkstyle

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThreadPool, QTimer, QSettings
from PyQt5.QtWidgets import (
    QMainWindow, QHBoxLayout,
    QDesktopWidget
)

# GUI
from .side_dock import SideDock
from .main_interface_tabs import MainInterfaceTabs
from .main_interface_menubar import MainInterfaceMenuBar
# Functions
from ..data import data as wgr_data
from ..func.wgr_api import WGR_API


class MainInterface(QMainWindow):
    # https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    sig_initGame = pyqtSignal(dict)

    def __init__(self, server, channel, cookies, realrun=True):
        super().__init__()
        self.server = server
        self.channel = channel
        self.cookies = cookies
        self.is_realrun = realrun
        self.side_dock_on = False

        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)
        self.threadpool = QThreadPool()
        self.api = WGR_API(self.server, self.channel, self.cookies)
        
        # !!! all DATA initialization must occur before any UI initialization !!!

        # TODO TODO multi-threading
        self.init_data_files()
        game_data = self.api_initGame()

        # TODO? if creates side dock first and ui later, the sign LineEdit cursor in side dock flashes (prob. Qt.Focus issue)
        self.init_ui()
        self.init_side_dock()
        if self.is_realrun:
            self.sig_initGame.connect(self.side_dock.on_received_resource)
            self.sig_initGame.connect(self.side_dock.on_received_name)
            self.sig_initGame.connect(self.side_dock.on_received_tasks)
            self.sig_initGame.connect(self.side_dock.on_received_lists)
            self.sig_initGame.emit(game_data)
        else:
            pass       


    # ================================
    # Initialization
    # ================================


    def set_color_scheme(self):
        self.setStyleSheet(wgr_data.get_color_scheme())

    def init_ui(self):
        self.set_color_scheme()
        user_w = QDesktopWidget().screenGeometry(-1).width()
        user_h = QDesktopWidget().screenGeometry(-1).height()
        self.resize(0.67*user_w, 0.67*user_h)

        self.menu_bar = MainInterfaceMenuBar(self)
        self.table_widget = MainInterfaceTabs(self, self.api, self.threadpool, self.is_realrun)

        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.table_widget)

        self.setLayout(QHBoxLayout())
        self.setWindowTitle('Warship Girls Viewer')

    def init_side_dock(self):
        def _create_side_dock():
            if self.side_dock_on == False:
                self.side_dock = SideDock(self, self.is_realrun)
                self.addDockWidget(Qt.RightDockWidgetArea, self.side_dock)
                self.side_dock_on = True
            else:
                pass

        if self.qsettings.contains("UI/init_side_dock"):
            if self.qsettings.value("UI/init_side_dock") == "true":
                pass
            else:
                _create_side_dock()
        else:
            self.qsettings.setValue("UI/init_side_dock", False)
            _create_side_dock()

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

    def api_initGame(self):
        test_json = os.path.join(wgr_data.get_temp_dir(), 'api_initGame.json')
        if self.is_realrun:
            data = self.api.api_initGame()
            with open(test_json, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            with open(test_json, encoding='utf-8') as f:
                data = json.load(f)

        # save necessary data; this should be done before any child UI creation!
        user_dir = wgr_data.get_user_dir()
        with open(os.path.join(user_dir, 'equipmentVo.json'), 'w', encoding='utf-8') as f:
            json.dump(data['equipmentVo'], f, ensure_ascii=False, indent=4)

        with open(os.path.join(user_dir, 'tactics.json'), 'w', encoding='utf-8') as f:
            json.dump(data['tactics'], f, ensure_ascii=False, indent=4)

        with open(os.path.join(user_dir, 'userVo.json'), 'w', encoding='utf-8') as f:
            json.dump(data['userVo'], f, ensure_ascii=False, indent=4)

        with open(os.path.join(user_dir, 'fleetVo.json'), 'w', encoding='utf-8') as f:
            json.dump(data['fleetVo'], f, ensure_ascii=False, indent=4)

        return data


# End of File