import os
import sys

from PyQt5.QtCore import Qt, pyqtSlot, QThreadPool, QSettings
from PyQt5.QtGui import QCloseEvent, QHideEvent
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from src import data as wgr_data
from src.gui.side_dock.dock import SideDock
from src.gui.interface.main_interface_tabs import MainInterfaceTabs
from src.gui.interface.main_interface_menubar import MainInterfaceMenuBar
from src.gui.system_tray import TrayIcon
from src.utils import get_app_version, get_user_resolution, _quit_application
from src.wgr.api import WGR_API


def init_zip_files() -> None:
    dir_size = sum(entry.stat().st_size for entry in os.scandir(wgr_data.get_zip_dir()))
    # E.zip + S.zip + init.zip ~= 34M+
    if dir_size < 30000000:
        wgr_data.init_resources()
    else:
        pass


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class MainInterface(QMainWindow):
    # https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect

    def __init__(self, cookies: dict, realrun: bool = True):
        super().__init__()
        self.cookies = cookies
        self.is_realrun = realrun

        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)
        self.threadpool = QThreadPool()
        self.api = WGR_API(self.cookies)

        # !!! all DATA initialization must occur before any UI initialization !!!

        # TODO TODO multi-threading
        init_zip_files()
        self.api_initGame()

        # TODO? if creates side dock first and ui later, the sign LineEdit cursor in side dock flashes (prob.
        #  Qt.Focus issue)
        # Tabs must be created before menu bar, as menu bar reference main_tabs
        self.main_tabs = MainInterfaceTabs(self, self.threadpool, self.is_realrun)
        self.menu_bar = MainInterfaceMenuBar(self)
        self.side_dock_on = False
        self.side_dock = None
        self.tray = None
        self.init_ui()
        self.init_side_dock()

    # ================================
    # Initialization
    # ================================

    def set_color_scheme(self) -> None:
        self.setStyleSheet(wgr_data.get_color_scheme())

    def init_ui(self) -> None:
        self.set_color_scheme()
        user_w, user_h = get_user_resolution()
        self.resize(int(0.67 * user_w), int(0.67 * user_h))

        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.main_tabs)

        self.setLayout(QHBoxLayout())
        self.setWindowTitle(f"Warship Girls Viewer v{get_app_version()}")

    def create_side_dock(self):
        if (self.side_dock_on is False) and (self.side_dock is None):
            self.side_dock = SideDock(self)
            self.addDockWidget(Qt.RightDockWidgetArea, self.side_dock)
            self.side_dock_on = True
        else:
            pass

    def init_side_dock(self) -> None:
        # Following only checks on log-in
        if self.qsettings.contains("UI/no_side_dock") is True:
            if self.qsettings.value("UI/no_side_dock") == "true":
                pass
            else:
                self.create_side_dock()
        else:
            self.qsettings.setValue("UI/no_side_dock", False)
            self.create_side_dock()

    def init_tray_icon(self) -> None:
        self.tray = TrayIcon(self, get_data_path('assets/favicon.ico'))

    # ================================
    # Events
    # ================================

    @pyqtSlot()
    def on_dock_closed(self) -> None:
        self.side_dock_on = False
        self.side_dock = None

    def closeEvent(self, event: QCloseEvent) -> None:
        _quit_application()

    def hideEvent(self, event: QHideEvent) -> None:
        self.hide()
        if self.tray is None:
            self.init_tray_icon()
        else:
            pass

    # ================================
    # WGR APIs
    # ================================

    def api_initGame(self) -> None:
        if self.is_realrun:
            data = self.api.initGame()
            wgr_data.save_api_initGame(data)
        else:
            data = wgr_data.get_api_initGame()

        wgr_data.save_equipmentVo(data['equipmentVo'])
        wgr_data.save_user_tactics(data['tactics'])
        wgr_data.save_userVo(data['userVo'])
        wgr_data.save_user_fleets(data['fleetVo'])
        wgr_data.save_pveExploreVo(data['pveExploreVo'])

# End of File
