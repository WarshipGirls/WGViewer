import logging
import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QGridLayout, QTabBar
)

from src.gui.tabs.advance_functions import TabAdvanceFunctions
from src.gui.tabs.tab_thermopylae import TabThermopylae
from src.gui.tabs.tab_ship import TabShips
from src.gui.tabs.tab_expedition import TabExpedition


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width() / self.count())
        return QSize(w, size.height())


class MainInterfaceTabs(QWidget):
    def __init__(self, parent, threadpool, is_realrun):
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

        self.add_tab("dock")
        self.add_tab("exp")
        self.add_tab("thermopylae")
        self.add_tab("adv")

        self.layout.addWidget(self.tabs, 0, 0)
        self.setLayout(self.layout)

    def init_ui(self) -> None:
        self.tabs.setTabBar(TabBar())
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

    def add_tab(self, dock_name: str) -> None:
        if dock_name is "dock":
            if self.tab_ships is not None:
                pass
            else:
                self.tab_ships = TabShips(self.is_realrun)
                self.tabs.addTab(self.tab_ships, "Dock")
        elif dock_name is "exp":
            if self.tab_exp is not None:
                pass
            else:
                self.tab_exp = TabExpedition()
                self.tabs.addTab(self.tab_exp, "Expedition (dev)")
        elif dock_name is "thermopylae":
            if self.tab_thermopylae is not None:
                pass
            else:
                self.tab_thermopylae = TabThermopylae()
                self.tabs.addTab(self.tab_thermopylae, "Thermopylae (dev")
        elif dock_name is "adv":
            if self.tab_adv is not None:
                pass
            else:
                self.tab_adv = TabAdvanceFunctions(self.parent)
                self.tabs.addTab(self.tab_adv, "Advance (N/A)")
        else:
            logging.error("TAB - Invalid tab name for creation.")

    def close_tab(self, index: int) -> None:
        tab = self.tabs.widget(index)
        logging.info(f'TAB - {tab.objectName()} is closed.')
        tab.deleteLater()
        self.tabs.removeTab(index)

# End of File
