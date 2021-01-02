import os
import sys

from PyQt5.QtCore import Qt, pyqtSlot, QThreadPool, QSettings
from PyQt5.QtGui import QCloseEvent, QHideEvent, QResizeEvent, QMoveEvent
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from src import data as wgv_data
from src import utils as wgv_utils
from src.func import qsettings_keys as QKEYS
from src.gui.side_dock.dock import SideDock
from src.gui.interface.tabs import MainInterfaceTabs
from src.gui.interface.menubar import MainInterfaceMenuBar
from src.gui.system_tray import TrayIcon
from src.utils import popup_msg
from src.wgr import WGR_API


def init_zip_files() -> None:
    dir_size = sum(entry.stat().st_size for entry in os.scandir(wgv_data.get_zip_dir()))
    # E.zip + S.zip + init.zip ~= 34M+
    if dir_size < 30000000:
        wgv_data.init_resources()
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

        self.qsettings = QSettings(wgv_data.get_qsettings_file(), QSettings.IniFormat)
        self.threadpool = QThreadPool()
        self.api = WGR_API(self.cookies)

        # !!! all DATA initialization must occur before any UI initialization !!!

        # TODO TODO multi-threading
        init_zip_files()
        self.api_initGame()

        # TODO? if creates side dock first and ui later, the sign LineEdit cursor in side dock flashes (prob.
        #  Qt.Focus issue)
        self.side_dock_on = False
        self.side_dock = None
        self.tray = None

        # 1. The init order cannot be changed right now
        #   tab_dock init all ships data and it's independent of side dock
        # 2. Tabs must be created before menu bar,  menu bar reference main_tabs
        self.main_tabs = MainInterfaceTabs(self, self.threadpool, self.is_realrun)
        # TODO loading speed is slow
        self.main_tabs.init_tab(QKEYS.UI_TAB_SHIP, 'tab_dock')
        self.init_side_dock()
        self.main_tabs.init_tab(QKEYS.UI_TAB_EXP, 'tab_exp')
        self.main_tabs.init_tab(QKEYS.UI_TAB_THER, 'tab_thermopylae')
        self.main_tabs.init_tab(QKEYS.UI_TAB_ADV, 'tab_adv')
        self.menu_bar = MainInterfaceMenuBar(self)
        self.init_ui()

    # ================================
    # Initialization
    # ================================

    def set_color_scheme(self) -> None:
        self.setStyleSheet(wgv_utils.get_color_scheme())

    def init_ui(self) -> None:
        self.set_color_scheme()
        if self.qsettings.contains(QKEYS.UI_MAIN) and self.qsettings.value(QKEYS.UI_MAIN, type=bool) is True:
            new_w = self.qsettings.value(QKEYS.UI_MAIN_W, type=int)
            new_h = self.qsettings.value(QKEYS.UI_MAIN_H, type=int)
            new_pos = self.qsettings.value(QKEYS.UI_MAIN_POS)
            self.resize(new_w, new_h)
            self.move(new_pos)
        else:
            user_w, user_h = wgv_utils.get_user_resolution()
            self.resize(int(0.67 * user_w), int(0.67 * user_h))

        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.main_tabs)

        self.setLayout(QHBoxLayout())
        self.setWindowTitle(f"Warship Girls Viewer v{wgv_utils.get_app_version()}")

    def create_side_dock(self) -> None:
        if self.side_dock is None:
            self.side_dock = SideDock(self, self.is_realrun)
        else:
            self.side_dock.show()
        if self.qsettings.contains(QKEYS.UI_SIDEDOCK_POS) is True:
            if self.qsettings.value(QKEYS.UI_SIDEDOCK_POS, type=int) == 0:
                pos = Qt.RightDockWidgetArea
            elif self.qsettings.value(QKEYS.UI_SIDEDOCK_POS, type=int) == 1:
                pos = Qt.LeftDockWidgetArea
            else:
                pos = Qt.RightDockWidgetArea
        else:
            pos = Qt.RightDockWidgetArea
        self.addDockWidget(pos, self.side_dock)

    def init_side_dock(self) -> None:
        self.create_side_dock()
        if self.qsettings.contains(QKEYS.UI_SIDEDOCK) is True:
            if self.qsettings.value(QKEYS.UI_SIDEDOCK, type=bool) is False:
                self.side_dock.hide()
            else:
                pass
        else:
            self.qsettings.setValue(QKEYS.UI_SIDEDOCK, True)

    def init_tray_icon(self) -> None:
        self.tray = TrayIcon(self, get_data_path('assets/favicon.ico'))

    # ================================
    # Events
    # ================================

    @pyqtSlot()
    def on_dock_closed(self) -> None:
        # self.side_dock_on = False
        # self.side_dock = None
        if self.side_dock.isVisible() is True:
            self.side_dock.hide()
        else:
            pass

    def closeEvent(self, event: QCloseEvent) -> None:
        wgv_utils.quit_application()

    def hideEvent(self, event: QHideEvent) -> None:
        self.hide()
        if self.tray is None:
            self.init_tray_icon()
        else:
            pass

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self.qsettings.contains(QKEYS.UI_MAIN) and self.qsettings.value(QKEYS.UI_MAIN, type=bool) is True:
            # sets value
            self.qsettings.setValue(QKEYS.UI_MAIN_W, self.width())
            self.qsettings.setValue(QKEYS.UI_MAIN_H, self.height())
        else:
            pass

    def moveEvent(self, event: QMoveEvent) -> None:
        if self.qsettings.contains(QKEYS.UI_MAIN) and self.qsettings.value(QKEYS.UI_MAIN, type=bool) is True:
            # sets value
            self.qsettings.setValue(QKEYS.UI_MAIN_POS, self.pos())
        else:
            pass

    # ================================
    # WGR APIs
    # ================================

    def api_initGame(self) -> None:
        if self.is_realrun:
            data = self.api.initGame()
            wgv_data.save_api_initGame(data)
        else:
            data = wgv_data.get_api_initGame()
        try:
            wgv_data.save_equipmentVo(data['equipmentVo'])
            wgv_data.save_user_tactics(data['tactics'])
            wgv_data.save_userVo(data['userVo'])
            wgv_data.save_user_fleets(data['fleetVo'])
            wgv_data.save_pveExploreVo(data['pveExploreVo'])
        except KeyError:
            popup_msg("Game data init failed...", "Init Error")
            # TODO? quit_application() not working
            sys.exit(-1)

# End of File
