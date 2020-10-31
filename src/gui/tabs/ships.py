import sys
import os
import logging

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtCore import pyqtSlot

from ...func import constants as CONST
from .ships_table import ShipTable
from .ships_top_checkbox import TopCheckboxes


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabShips(QWidget):
    def __init__(self, realrun):
        super().__init__()

        list_box = QVBoxLayout(self)
        self.setLayout(list_box)

        scroll = QScrollArea(self)
        list_box.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)

        self.scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(self.scroll_layout)
        scroll.setWidget(scroll_content)

        # only 20 out of 27 is used by the game at 5.0.0
        # self.ships = [[]] * 27    # this binds to same list
        self.ships = []
        for i in range(27):
            self.ships.append([])
        # TODO? https://github.com/WarshipGirls/WGViewer/issues/7
        self.ship_table = ShipTable()
        ck = TopCheckboxes(self.ship_table)

        self.scroll_layout.addWidget(ck)
        self.scroll_layout.addWidget(self.ship_table)

        self.scroll_layout.setStretch(0, 1)
        self.scroll_layout.setStretch(1, 10)   # Give space to the table as much as possible

        if realrun == 0:
            self.test()
        print("tabships")
        # self.setFixedHeight(200)
        print(self.width(), self.height())

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
            for s in sorted_ships:
                self.ships[s["type"]].append(s)

            for ship_type, ship_lists in enumerate(self.ships):
                if (ship_type not in CONST.ship_type) and (len(ship_lists) != 0):
                    continue
                else:
                    for ship in ship_lists:
                        self.ship_table.insertRow(self.ship_table.rowCount())
                        self.ship_table.add_ship(self.ship_table.rowCount()-1, ship)


# End of File