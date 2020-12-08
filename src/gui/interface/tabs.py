import logging
import os
import sys

from PyQt5.QtCore import QSize, Qt, QThreadPool
from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QGridLayout, QTabBar
)

from src.gui.tabs.advance_functions import TabAdvanceFunctions
from src.gui.tabs.tab_thermopylae import TabThermopylae
from src.gui.tabs.tab_ship import TabShips
from src.gui.tabs.tab_expedition import TabExpedition


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
        logging.info("Creating Main Interface Tabs...")
        self.parent = parent
        self.threadpool = threadpool
        self.is_realrun = is_realrun

        # do NOT change the order of creation
        self.layout = QGridLayout()
        self.tab_ships = None
        self.tab_exp = None
        self.tab_adv = None
        self.tab_thermopylae = None
        self.tabs = QTabWidget()
        self.tabs.setTabBar(QTabBar())
        self.init_ui()

        # TODO now tab_dock init important data
        #   either make tab dock as default (must run)
        #   or run tab dock functions save & load important data later
        if self.is_realrun is True:
            # TODO loading speed is really slow
            # self.add_tab("tab_dock")
            # self.add_tab("tab_exp")
            self.add_tab("tab_thermopylae")
            # self.add_tab("tab_adv")
            # pass
        else:
            # self.add_tab("tab_dock")
            self.add_tab("tab_thermopylae")
            # self.add_tab("tab_adv")

        self.layout.addWidget(self.tabs, 0, 0)
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

    def add_tab(self, tab_name: str) -> None:
        logging.info(f"TAB - Creating {tab_name}")
        if tab_name == "tab_adv" and self.tab_adv is None:
            self.tab_adv = TabAdvanceFunctions(tab_name, self.parent.side_dock)
            self.tabs.addTab(self.tab_adv, "Advance (N/A)")
        elif tab_name == "tab_dock" and self.tab_ships is None:
            self.tab_ships = TabShips(tab_name, self.is_realrun)
            self.tabs.addTab(self.tab_ships, "Dock")
        elif tab_name == "tab_exp" and self.tab_exp is None:
            self.tab_exp = TabExpedition(tab_name)
            self.tabs.addTab(self.tab_exp, "Expedition (dev)")
        elif tab_name == "tab_thermopylae" and self.tab_thermopylae is None:
            self.tab_thermopylae = TabThermopylae(tab_name, self.parent.side_dock, self.is_realrun)
            self.tabs.addTab(self.tab_thermopylae, "Thermopylae (dev)")
        else:
            logging.error(f"TAB - Invalid tab name {tab_name} for creation.")

    def close_tab(self, index: int) -> None:
        tab = self.tabs.widget(index)
        logging.info(f'TAB - {tab.objectName()} is closed.')

        # TODO reopen tab will create a new object
        #   should we save the old data
        #   or let the user decide?

        self.reset_tab_object(tab.objectName())
        tab.deleteLater()
        self.tabs.removeTab(index)

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
            logging.error(f"TAB - Failed to reset {tab_obj_name} to None.")


# End of File
