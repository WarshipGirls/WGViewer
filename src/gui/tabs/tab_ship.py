import logging
import os
import sys
import zipfile

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QLineEdit,
    QVBoxLayout, QGridLayout, QScrollArea,
    QHeaderView, QTableView
)

from src import data as wgr_data
from .ships.delegate import ShipTableDelegate
from .ships.model import ShipModel
from .ships.proxy_model import ShipSortFilterProxyModel
from .ships.top_checkbox import TopCheckboxes


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QWidget):
    def __init__(self, api, is_realrun):
        super().__init__()
        logging.info("SHIPS - Creating Ships Tab...")
        self.api = api

        self.content_widget = None
        self.content_layout = None
        self.upper_content_widget = None
        self.lower_content_widget = None
        self.table_view = None
        self.table_model = None
        self.table_proxy = None
        self.lower_layout = None
        self.search_line = None
        self.init_ui()
        self.init_assets()

        if is_realrun:
            self._realrun()
        else:
            self._testrun()

    def _realrun(self):
        data = self.api.api_getShipList()
        wgr_data.save_api_getShipList(data)
        self.on_received_shiplist(data)

    def _testrun(self):
        logging.debug("SHIPS - Starting tests...")
        data = wgr_data.get_api_getShipList()
        # logging.error(len(data['userShipVO']))
        # data['userShipVO'] = data['userShipVO'][:5]
        self.on_received_shiplist(data)

    def init_ui(self):
        scroll_box = QVBoxLayout(self)
        self.setLayout(scroll_box)
        scroll = QScrollArea(self)
        scroll_box.addWidget(scroll)
        scroll.setWidgetResizable(True)

        self.content_widget = QWidget(scroll)

        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setLayout(self.content_layout)
        scroll.setWidget(self.content_widget)

        self.upper_content_widget = QWidget(self.content_widget)
        self.lower_content_widget = QWidget(self.content_widget)

        self.content_layout.addWidget(self.upper_content_widget)
        self.content_layout.addWidget(self.lower_content_widget)
        self.content_layout.setStretch(0, 1)
        self.content_layout.setStretch(1, 10)

        self.table_view = QTableView(self.lower_content_widget)
        self.table_model = ShipModel(self.table_view, self.api)
        self.table_proxy = ShipSortFilterProxyModel(self)
        self.table_proxy.setSourceModel(self.table_model)
        self.table_view.setModel(self.table_proxy)
        TopCheckboxes(self.upper_content_widget, self.table_model, self.table_proxy)

        self.lower_layout = QGridLayout(self.lower_content_widget)
        self.search_line = QLineEdit(self.lower_content_widget)
        self.search_line.setPlaceholderText('Search ship by name. To reset, type whitespace and delete it.')
        self.search_line.textChanged.connect(self.table_proxy.set_name_filter)
        self.lower_layout.addWidget(self.search_line, 0, 0, 1, self.table_model.columnCount())
        self.lower_layout.addWidget(self.table_view, 1, 0, 1, self.table_model.columnCount())

        self.init_view_settings()

    def init_view_settings(self):
        self.table_view.setItemDelegate(ShipTableDelegate(self.table_view))

        self.table_view.setSortingEnabled(True)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setShowGrid(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    @staticmethod
    def init_assets():
        # TODO: find drive that serves ppl in/out GFW
        # TODO: pyinstaller seems not packing zip
        # s_link = 'https://drive.google.com/file/d/1v5VO1b_Phl66xJJgk4TAXjGa_XHjbl-k/view?usp=sharing'
        # e_link = 'https://drive.google.com/file/d/1CeluorrRqqhrKeNUo18UelKXhTxE8dsU/view?usp=sharing'
        logging.info('SHIPS - Loading necessary assets files...')
        if os.path.isdir(get_data_path('assets/S')):
            pass
        else:
            with zipfile.ZipFile(get_data_path('assets/S.zip'), 'r') as zip_ref:
                zip_ref.extractall(get_data_path('assets'))

        if os.path.isdir(get_data_path('assets/E')):
            pass
        else:
            with zipfile.ZipFile(get_data_path('assets/E.zip'), 'r') as zip_ref:
                zip_ref.extractall(get_data_path('assets'))

    @pyqtSlot(dict)
    def on_received_shiplist(self, data):
        if data is None:
            logging.error("SHIPS - Invalid ship list data.")
        else:
            # First sort by level, then sort by cid
            sorted_ships = sorted(data["userShipVO"], key=lambda x: (x['level'], x['shipCid']), reverse=True)
            self.table_model.set_data(sorted_ships)
            self.table_model.save_table_data()
            logging.info("SHIPS - Success initialized table and saved table data.")

# End of File
