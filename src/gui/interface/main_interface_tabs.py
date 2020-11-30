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
    def __init__(self, parent, api, threadpool, is_realrun):
        super().__init__()
        logging.info("Creating Main Interface Tabs...")
        self.api = api
        self.parent = parent
        self.threadpool = threadpool
        self.is_realrun = is_realrun

        # do NOT change the order of creation
        self.layout = QGridLayout()
        self.tab_ships = TabShips(self.api, self.is_realrun)
        self.tab_exp = TabExpedition()
        self.tab_adv = TabAdvanceFunctions(self.parent)
        self.tab_thermopylae = TabThermopylae()
        self.tabs = QTabWidget()
        self.tabs.setTabBar(QTabBar())
        self.init_ui()

        self.tabs.addTab(self.tab_thermopylae, "Thermopylae")
        self.tabs.addTab(self.tab_exp, "Expedition (beta)")
        self.tabs.addTab(self.tab_ships, "Dock")
        self.tabs.addTab(self.tab_adv, "Advance (N/A)")

        self.layout.addWidget(self.tabs, 0, 0)
        self.setLayout(self.layout)

    def init_ui(self):
        self.tabs.setTabBar(TabBar())
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tabs.removeTab(index)

# End of File
