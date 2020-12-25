import os
import sys

from PyQt5.QtCore import QSize, Qt, QThreadPool, QSettings
from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QGridLayout, QTabBar, QLabel
)

from src.data import get_qsettings_file
from src.func import qsettings_keys as QKEYS
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from src.gui.tabs.advance_functions import TabAdvanceFunctions
from src.gui.tabs.tab_thermopylae import TabThermopylae
from src.gui.tabs.tab_ship import TabShips
from src.gui.tabs.tab_expedition import TabExpedition

logger = get_logger(QLOGS.TABS)


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabBar(QTabBar):
    def tabSizeHint(self, index: int) -> QSize:
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width() / self.count())
        return QSize(w, size.height())


class MainInterfaceTabs(QWidget):
    def __init__(self, parent, threadpool: QThreadPool, is_realrun: bool):
        super().__init__()
        logger.info("Creating Main Interface Tabs...")
        self.parent = parent
        self.threadpool = threadpool
        self.is_realrun = is_realrun

        self.qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
        self.has_tab = False

        # do NOT change the order of creation
        self.layout = QGridLayout()
        self.tab_ships = None
        self.tab_exp = None
        self.tab_adv = None
        self.tab_thermopylae = None
        self.tabs = QTabWidget()
        self._msg_label = None
        self.init_ui()

        self.layout.addWidget(self.tabs, 0, 0)
        if self.has_tab is True:
            pass
        else:
            self.add_warning_message()
        self.setLayout(self.layout)

    def init_ui(self) -> None:
        self.tabs.setTabBar(TabBar())
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setTabBarAutoHide(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

    def init_tab(self, key: str, obj_name: str) -> None:
        if self.qsettings.contains(key):
            if self.qsettings.value(key, type=bool) is True:
                self.add_tab(obj_name)
            else:
                pass
        else:
            self.add_tab(obj_name)

    def add_warning_message(self):
        self._msg_label = self.get_warning_message()
        self.layout.addWidget(self._msg_label)

    def add_tab(self, tab_name: str) -> None:
        if self._msg_label is None:
            pass
        else:
            self.layout.removeWidget(self._msg_label)
            self._msg_label.deleteLater()
            self._msg_label = None

        self.has_tab = True

        logger.debug(f"Creating {tab_name}")
        if tab_name == "tab_adv" and self.tab_adv is None:
            self.tab_adv = TabAdvanceFunctions(tab_name, self.parent.side_dock)
            self.tabs.addTab(self.tab_adv, "Advance (N/A)")
        elif tab_name == "tab_dock" and self.tab_ships is None:
            # NOTE: tab_dock cannot be dependent on side dock
            self.tab_ships = TabShips(tab_name, self.is_realrun)
            self.tabs.addTab(self.tab_ships, "Dock")
        elif tab_name == "tab_exp" and self.tab_exp is None:
            self.tab_exp = TabExpedition(tab_name, self.parent.side_dock)
            self.tabs.addTab(self.tab_exp, "Expedition (dev)")
        elif tab_name == "tab_thermopylae" and self.tab_thermopylae is None:
            self.tab_thermopylae = TabThermopylae(tab_name, self.parent.side_dock, self.is_realrun)
            self.tabs.addTab(self.tab_thermopylae, "Thermopylae")
        else:
            logger.error(f"Invalid tab name {tab_name} for creation.")

    def close_tab(self, index: int) -> None:
        tab = self.tabs.widget(index)
        logger.debug(f'{tab.objectName()} is closed.')

        # TODO reopen tab will create a new object
        #   should we save the old data, or let the user decide?

        self.reset_tab_object(tab.objectName())
        tab.deleteLater()
        self.tabs.removeTab(index)

        if self.tabs.count() == 0:
            self.add_warning_message()
            self.has_tab = False
        else:
            pass

    @staticmethod
    def get_warning_message() -> QLabel:
        _msg = "No tabs are selected to show on startup.\n"
        _msg += "Open tabs: \tTop Menu Bar -> View -> Tabs -> ...\n"
        _msg += "Change settings: \tTop Menu Bar -> File -> Settings -> UI -> ..."
        return QLabel(_msg)

    def reset_tab_object(self, tab_obj_name: str) -> None:
        # Lesson: `is` for pointing to the same object, `==` for pointing to the same value
        if tab_obj_name == "tab_adv":
            self.tab_adv = None
        elif tab_obj_name == "tab_dock":
            self.tab_ships = None
        elif tab_obj_name == "tab_exp":
            self.tab_exp = None
        elif tab_obj_name == "tab_thermopylae":
            self.tab_thermopylae = None
        else:
            logger.debug(f"Failed to reset {tab_obj_name} to None.")


# End of File
