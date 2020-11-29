import os

from PyQt5.QtCore import Qt, pyqtSlot, QThreadPool, QSettings
from PyQt5.QtWidgets import (
    QMainWindow, QHBoxLayout,
    QDesktopWidget
)

from src import data as wgr_data
from src.func.wgr_api import WGR_API
from src.gui.side_dock.dock import SideDock
from src.gui.interface.main_interface_tabs import MainInterfaceTabs
from src.gui.interface.main_interface_menubar import MainInterfaceMenuBar


def init_data_files():
    num = len(os.listdir(wgr_data.get_init_dir()))
    # As of 5.0.0, there should be 30 files
    if num != 30:
        wgr_data.save_init_data()
    else:
        pass


class MainInterface(QMainWindow):
    # https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    # sig_initGame = pyqtSignal(dict)

    def __init__(self, server, channel, cookies, realrun=True):
        super().__init__()
        self.server = server
        self.channel = channel
        self.cookies = cookies
        self.is_realrun = realrun

        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)
        self.threadpool = QThreadPool()
        self.api = WGR_API(self.server, self.channel, self.cookies)

        # !!! all DATA initialization must occur before any UI initialization !!!

        # TODO TODO multi-threading
        init_data_files()
        self.api_initGame()

        # TODO? if creates side dock first and ui later, the sign LineEdit cursor in side dock flashes (prob.
        #  Qt.Focus issue)
        self.menu_bar = MainInterfaceMenuBar(self)
        self.table_widget = MainInterfaceTabs(self, self.api, self.threadpool, self.is_realrun)
        self.side_dock_on = False
        self.side_dock = None
        self.init_ui()
        self.init_side_dock()

    # ================================
    # Initialization
    # ================================

    def set_color_scheme(self):
        self.setStyleSheet(wgr_data.get_color_scheme())

    def init_ui(self):
        self.set_color_scheme()
        user_w = QDesktopWidget().screenGeometry(-1).width()
        user_h = QDesktopWidget().screenGeometry(-1).height()
        self.resize(0.67 * user_w, 0.67 * user_h)

        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.table_widget)

        self.setLayout(QHBoxLayout())
        self.setWindowTitle('Warship Girls Viewer')

    def init_side_dock(self):
        def _create_side_dock():
            if (self.side_dock_on is False) and (self.side_dock is None):
                self.side_dock = SideDock(self)
                self.addDockWidget(Qt.RightDockWidgetArea, self.side_dock)
                self.side_dock_on = True
            else:
                pass

        if self.qsettings.contains("UI/no_side_dock") is True:
            if self.qsettings.value("UI/no_side_dock") == "true":
                pass
            else:
                _create_side_dock()
        else:
            self.qsettings.setValue("UI/no_side_dock", False)
            _create_side_dock()

    # ================================
    # Events
    # ================================

    @pyqtSlot()
    def on_dock_closed(self):
        self.side_dock_on = False
        self.side_dock = None

    # ================================
    # WGR APIs
    # ================================

    def api_initGame(self):
        if self.is_realrun:
            data = self.api.api_initGame()
            wgr_data.save_api_initGame(data)
        else:
            data = wgr_data.get_api_initGame()

        wgr_data.save_equipmentVo(data['equipmentVo'])
        wgr_data.save_user_tactics(data['tactics'])
        wgr_data.save_userVo(data['userVo'])
        wgr_data.save_user_fleets(data['fleetVo'])
        wgr_data.save_pveExploreVo(data['pveExploreVo'])

# End of File
