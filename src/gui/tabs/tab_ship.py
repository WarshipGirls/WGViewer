import os
import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QLineEdit,
    QVBoxLayout, QGridLayout, QScrollArea,
    QHeaderView, QTableView
)

from src import data as wgv_data
from src.wgr.api import WGR_API
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from .ships.delegate import ShipTableDelegate
from .ships.model import ShipModel
from .ships.proxy_model import ShipSortFilterProxyModel
from .ships.top_checkbox import TopCheckboxes

logger = get_logger(QLOGS.TAB_SHIP)


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QWidget):
    def __init__(self, tab_name: str, is_realrun: bool):
        super().__init__()
        logger.info("Creating Ships Tab...")
        self.api = WGR_API(wgv_data.load_cookies())

        self.setObjectName(tab_name)
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

        if is_realrun:
            self._realrun()
        else:
            self._testrun()

    def _realrun(self) -> None:
        data = self.api.getShipList()
        wgv_data.save_api_getShipList(data)
        self.on_received_shiplist(data)

    def _testrun(self) -> None:
        logger.debug("Starting tests...")
        data = wgv_data.get_api_getShipList()
        # logger.error(len(data['userShipVO']))
        # data['userShipVO'] = data['userShipVO'][:5]
        self.on_received_shiplist(data)

    def init_ui(self) -> None:
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
        self.table_model = ShipModel(self.table_view)
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

    def init_view_settings(self) -> None:
        self.table_view.setItemDelegate(ShipTableDelegate(self.table_view))

        self.table_view.setSortingEnabled(True)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setShowGrid(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    @pyqtSlot(dict)
    def on_received_shiplist(self, data) -> None:
        if data is None:
            logger.error("Invalid ship list data.")
        else:
            # First sort by level, then sort by cid
            sorted_ships = sorted(data["userShipVO"], key=lambda x: (x['level'], x['shipCid']), reverse=True)
            self.table_model.set_data(sorted_ships)
            self.table_model.save_table_data()
            logger.info("Success initialized table and saved table data.")

# End of File
