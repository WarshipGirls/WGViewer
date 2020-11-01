import sys
import os
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QScrollArea, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QCheckBox, QTableView
from PyQt5.QtCore import Qt, pyqtSlot, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from ...func import constants as CONST
from .ships_table import ShipTable, ShipTableDelegate
from .ships_top_checkbox import TopCheckboxes


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QWidget):
    def __init__(self, realrun):
        super().__init__()

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

        ck = TopCheckboxes(self.upper_content_widget, 0)

        self.table_view = QTableView(self.lower_content_widget)
        self.lower_layout = QGridLayout(self.lower_content_widget)
        self.lower_layout.addWidget(self.table_view, 0, 0, 1, 20)
        self.table_model = QStandardItemModel(self)

        for rowName in range(15*10):
            self.table_model.invisibleRootItem().appendRow(
                [   QStandardItem("row {0} col {1}".format(rowName, column))    
                    for column in range(20)
                    ]
                )

        self.table_proxy = QSortFilterProxyModel(self)
        self.table_proxy.setSourceModel(self.table_model)

        self.table_view.setModel(self.table_proxy)
        self.table_view.setItemDelegate(ShipTableDelegate(self.table_view))
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # self.content_widget  = QtWidgets.QWidget(self)
        # self.lineEdit       = QtWidgets.QLineEdit(self.content_widget)
        # self.view           = QtWidgets.QTableView(self.content_widget)
        # self.comboBox       = QtWidgets.QComboBox(self.content_widget)
        # self.label          = QtWidgets.QLabel(self.content_widget)

        # self.gridLayout = QtWidgets.QGridLayout(self.content_widget)
        # self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        # self.gridLayout.addWidget(self.view, 1, 0, 1, 3)
        # self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        # self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        # # self.setcontent_widget(self.content_widget)
        # self.label.setText("Regex Filter")
        # self.model = QtGui.QStandardItemModel(self)
        # for rowName in range(3*5):
        #     self.model.invisibleRootItem().appendRow(
        #         [   QtGui.QStandardItem("row {0} col {1}".format(rowName, column))    
        #             for column in range(3)
        #             ]
        #         )

        # self.proxy = QtCore.QSortFilterProxyModel(self)
        # self.proxy.setSourceModel(self.model)

        # self.view.setModel(self.proxy)
        # self.comboBox.addItems(["Column {0}".format(x) for x in range(self.model.columnCount())])


    #     list_box = QVBoxLayout(self)
    #     self.setLayout(list_box)

    #     scroll = QScrollArea(self)
    #     list_box.addWidget(scroll)
    #     scroll.setWidgetResizable(True)
    #     scroll_content = QWidget(scroll)

    #     self.scroll_layout = QVBoxLayout(scroll_content)
    #     scroll_content.setLayout(self.scroll_layout)
    #     scroll.setWidget(scroll_content)

    #     # only 20 out of 27 is used by the game at 5.0.0
    #     # self.ships = [[]] * 27    # this binds to same list
    #     self.ships = []
    #     for i in range(27):
    #         self.ships.append([])
    #     # TODO? https://github.com/WarshipGirls/WGViewer/issues/7
    #     self.ship_table = ShipTable()
    #     ck = TopCheckboxes(self.ship_table)

    #     self.scroll_layout.addWidget(ck)
    #     self.scroll_layout.addWidget(self.ship_table)

    #     self.scroll_layout.setStretch(0, 1)
    #     self.scroll_layout.setStretch(1, 10)   # Give space to the table as much as possible

    #     if realrun == 0:
    #         self.test()
    #     print("tabships")
    #     # self.setFixedHeight(200)
    #     print(self.width(), self.height())

    # def test(self):
    #     logging.debug("Starting tests")
    #     import json
    #     p = get_data_path('api_getShipList.json')
    #     with open(p) as f:
    #         d = json.load(f)
    #     self.on_received_shiplist(d)

    # @pyqtSlot(dict)
    # def on_received_shiplist(self, data):
    #     if data == None:
    #         logging.error("Invalid ship list data.")
    #     else:
    #         # First sort by level, then sort by cid
    #         sorted_ships = sorted(data["userShipVO"], key=lambda x: (x['level'], x['shipCid']), reverse=True)
    #         for s in sorted_ships:
    #             self.ships[s["type"]].append(s)

    #         for ship_type, ship_lists in enumerate(self.ships):
    #             if (ship_type not in CONST.ship_type) and (len(ship_lists) != 0):
    #                 continue
    #             else:
    #                 for ship in ship_lists:
    #                     self.ship_table.insertRow(self.ship_table.rowCount())
    #                     self.ship_table.add_ship(self.ship_table.rowCount()-1, ship)


# End of File