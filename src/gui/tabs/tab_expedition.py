import os
import sys

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from .expedition.table import ExpTable
from .expedition.summary import DailySummary
from .expedition.fleets import ExpFleets

logger = get_logger(QLOGS.TAB_EXP)


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabExpedition(QWidget):
    def __init__(self, tab_name: str):
        super().__init__()
        self.setObjectName(tab_name)
        csv_path = get_data_path('assets/data/exp_data.csv')
        self.table = ExpTable(csv_path)
        self.summary = DailySummary()
        self.fleet_table = ExpFleets()
        logger.info("Creating Expedition Tab...")
        self.init_ui()

    def init_ui(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.table)
        left_layout.addWidget(self.summary)
        left_layout.setStretch(0, 1)
        left_layout.setStretch(1, 0)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.fleet_table)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 0)

        self.setLayout(main_layout)

# End of File
