import sys
import os
import logging
import zipfile

from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QHeaderView, QTableView
from PyQt5.QtCore import Qt, pyqtSlot

from .ships_delegate import ShipTableDelegate
from .ships_proxy_model import ShipSortFilterProxyModel
from .ships_top_checkbox import TopCheckboxes
from .ships_model import ShipModel


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QWidget):
    def __init__(self, api, realrun):
        super().__init__()
        self.api = api

        self.init_ui()
        self.init_assets()

        if realrun == 0:
            self.test()

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
        ck = TopCheckboxes(self.upper_content_widget, self.table_model, self.table_proxy)

        self.lower_layout = QGridLayout(self.lower_content_widget)
        self.search_line = QLineEdit(self.lower_content_widget)
        self.lower_layout.addWidget(self.search_line, 0, 0, 1, 1)
        self.lower_layout.addWidget(self.table_view, 1, 0, 1, self.table_model.columnCount())

        self.init_view_settings()

        header = self.table_view.horizontalHeader()
        for i in range(self.table_model.columnCount()):
            # QHeaderView.Stretch
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.search_line.textChanged.connect(self.table_proxy.setNameFilter)

    def init_view_settings(self):
        self.table_view.setItemDelegate(ShipTableDelegate(self.table_view))

        self.table_view.setSortingEnabled(True)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setShowGrid(False)

    def init_assets(self):
        # TODO: find drive that serves ppl in/out GFW
        # s_link = 'https://drive.google.com/file/d/1v5VO1b_Phl66xJJgk4TAXjGa_XHjbl-k/view?usp=sharing'
        # e_link = 'https://drive.google.com/file/d/1CeluorrRqqhrKeNUo18UelKXhTxE8dsU/view?usp=sharing'
        logging.info('Loading necessary resource files...')
        if os.path.isdir(get_data_path('src/assets/S')):
            pass
        else:
            with zipfile.ZipFile(get_data_path('src/assets/S.zip'), 'r') as zip_ref:
                zip_ref.extractall(get_data_path('src/assets'))

        if os.path.isdir(get_data_path('src/assets/E')):
            pass
        else:
            with zipfile.ZipFile(get_data_path('src/assets/E.zip'), 'r') as zip_ref:
                zip_ref.extractall(get_data_path('src/assets'))

    def test(self):
        logging.debug("Starting tests")
        import json
        p = get_data_path('api_getShipList.json')
        with open(p) as f:
            d = json.load(f)
        self.on_received_shiplist(d)

    @pyqtSlot(dict)
    def on_received_shiplist(self, data):
        if data == None:
            logging.error("Invalid ship list data.")
        else:
            # First sort by level, then sort by cid
            sorted_ships = sorted(data["userShipVO"], key=lambda x: (x['level'], x['shipCid']), reverse=True)
            self.table_model.set_data(sorted_ships)


# End of File