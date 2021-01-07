import os
import sys

from PyQt5.QtCore import Qt, pyqtSlot, QThreadPool, QSettings, pyqtSignal
from PyQt5.QtGui import QCloseEvent, QHideEvent, QResizeEvent, QMoveEvent
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from src import data as wgv_data
from src import utils as wgv_utils
from src.exceptions.wgr_error import get_error_text
from src.func import qsettings_keys as QKEYS
from src.func.worker import CallbackWorker
from src.gui.custom_widgets import QtProgressBar
from src.gui.side_dock.dock import SideDock
from src.gui.interface.tabs import MainInterfaceTabs
from src.gui.interface.menubar import MainInterfaceMenuBar
from src.gui.system_tray import TrayIcon
from src.wgr import WGR_API


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class MainInterface(QMainWindow):
    """
    Main Interface of WGViewer. The entry point of all functional QWidgets (tabs, side dock...).

    @note:
        - all data initialization must occur before any UI initialization
    @todo:
        - if creates side dock first and ui later, the sign LineEdit cursor in side dock flashes (prob. Qt.Focus issue)
    """

    # https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    sig_progress_bar = pyqtSignal(int)

    def __init__(self, cookies: dict, login_form: pyqtSignal, realrun: bool = True):
        super().__init__()
        self.hide()
        self.cookies = cookies
        self.sig_close_login = login_form
        self.is_realrun = realrun

        self.qsettings = QSettings(wgv_data.get_qsettings_file(), QSettings.IniFormat)
        self.threadpool = QThreadPool.globalInstance()
        self.api = WGR_API(self.cookies)

        self.side_dock_on = False
        self.side_dock = None
        self.tray = None
        self.main_tabs = None
        self.menu_bar = None
        # This widget is deleted upon completion
        self.progress_bar = QtProgressBar(self, title="Downloading Essential Resource Zips")
        self.sig_progress_bar.connect(self.progress_bar.update_value)
        # This bee is deleted upon completion
        self.bee_download_zip = CallbackWorker(self.init_zip_files, ([self.sig_progress_bar]), self.zip_download_finished)
        self.bee_download_zip.terminate()

    def start_rendering(self) -> None:
        self.progress_bar.show()
        self.bee_download_zip.start()

    def zip_download_finished(self, res: bool) -> None:
        self.progress_bar.close()
        self.progress_bar = None
        del self.progress_bar
        self.bee_download_zip = None
        del self.bee_download_zip
        self.show()
        if self.sig_close_login is not None:
            self.sig_close_login.emit()
            self.sig_close_login = None
            del self.sig_close_login
        else:
            pass

        if res is True:
            # Original UI initialization sequence
            self.api_initGame()
            # 1. The init order cannot be changed right now
            #   tab_dock init all ships data and it's independent of side dock
            # 2. Tabs must be created before menu bar,  menu bar reference main_tabs
            self.main_tabs = MainInterfaceTabs(self, self.is_realrun)
            # TODO loading speed is slow
            self.main_tabs.init_tab(QKEYS.UI_TAB_SHIP, 'tab_dock')
            self.init_side_dock()
            self.main_tabs.init_tab(QKEYS.UI_TAB_EXP, 'tab_exp')
            self.main_tabs.init_tab(QKEYS.UI_TAB_THER, 'tab_thermopylae')
            self.main_tabs.init_tab(QKEYS.UI_TAB_ADV, 'tab_adv')
            self.menu_bar = MainInterfaceMenuBar(self)
            self.init_ui()
        else:
            wgv_utils.popup_msg("Failed to download essential zip resources.")

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

    @staticmethod
    def get_zip_files_size() -> int:
        # E.zip + S.zip + init.zip ~= 34M+
        dir_size = sum(entry.stat().st_size for entry in os.scandir(wgv_data.get_zip_dir()))
        return dir_size

    def init_zip_files(self, progress_bar: pyqtSignal) -> bool:
        dir_size = self.get_zip_files_size()
        if dir_size < 30000000:
            wgv_data.init_resources(progress_bar)
            # Re-assess folder size after downloading
            dir_size = self.get_zip_files_size()
            if dir_size < 30000000:
                res = False
            else:
                res = True
        else:
            res = True
        return res

    # ================================
    # WGR APIs
    # ================================

    def api_initGame(self) -> None:
        if self.is_realrun:
            data = self.api.initGame()
            wgv_data.save_api_initGame(data)
        else:
            data = wgv_data.get_api_initGame()

        if 'eid' in data:
            wgv_utils.popup_msg(get_error_text(data['eid']), "Init Error")
            sys.exit(-1)

        try:
            wgv_data.save_equipmentVo(data['equipmentVo'])
            wgv_data.save_user_tactics(data['tactics'])
            wgv_data.save_userVo(data['userVo'])
            wgv_data.save_user_fleets(data['fleetVo'])
            wgv_data.save_pveExploreVo(data['pveExploreVo'])
        except KeyError:
            wgv_utils.popup_msg("Game data init failed...", "Init Error")
            # TODO? quit_application() not working
            sys.exit(-1)

# End of File
