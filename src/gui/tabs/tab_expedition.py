import logging
import os
import sys

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QGridLayout

from .expedition.table import ExpTable
from .expedition.summary import DailySummary
from .expedition.fleets import ExpFleets


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabExpedition(QWidget):
    def __init__(self):
        super().__init__()
        logging.info("Creating Expedition Tab...")
        self.init_ui()

    def init_ui(self):
        main_layout = QGridLayout(self)

        csv_path = get_data_path('assets/data/exp_data.csv')

        self.table = ExpTable(csv_path)
        main_layout.addWidget(self.table, 0, 0, self.table.get_row_count(), self.table.get_col_count())

        self.fleet_table = ExpFleets()
        main_layout.addWidget(self.fleet_table, 0, self.table.get_col_count(), self.fleet_table.get_row_count(), self.fleet_table.get_col_count())

        self.summary = DailySummary()
        main_layout.addWidget(self.summary, self.table.get_row_count(), 0, 5, 10)

        self.setLayout(main_layout)


# End of File