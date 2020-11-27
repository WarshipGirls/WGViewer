import os
import sys

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QGridLayout

from .expedition.table import ExpTable


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabExpedition(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QGridLayout(self)

        csv_path = get_data_path('src/assets/data/exp_data.csv')

        self.table = ExpTable(self, csv_path)
        main_layout.addWidget(self.table, 0, 0, self.table.get_row_count(), self.table.get_col_count())

        test = QLabel("asdf")
        main_layout.addWidget(test, 0, self.table.get_col_count(), 1, 1)

        self.setLayout(main_layout)


# End of File