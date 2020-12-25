import csv
import os
from logging import Logger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QTableView, QHeaderView, QAbstractScrollArea
)

from src.data import get_expedition_log


class DailySummary(QTableWidget):
    """
    Provide a summary table of expedition regarding daily and weekly sums, respectively.
        Due to the data I/O characteristics, it is local timezone-aware and is automatically
        refreshed upon a new day and a new week.
    """

    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

        self.day_values: list = [0] * 8
        self.week_values: list = [0] * 8

        self.init_table()
        self.init_ui()

    # ================================
    # UI
    # ================================

    def init_table(self) -> None:
        self.setColumnCount(4)
        self.setRowCount(10)

        self.setItem(0, 0, QTableWidgetItem("DAILY SUMMARY"))
        self.setItem(5, 0, QTableWidgetItem("WEEKLY SUMMARY"))
        self.setSpan(0, 0, 1, 4)
        self.setSpan(5, 0, 1, 4)

        labels_col1 = ["Fuel", "Ammo.", "Steel", "Bauxite"]
        labels_col2 = ["Inst. Repair", "Inst. Build.", "Ship Blueprint", "Equip. Blueprint"]
        w_path, d_path = get_expedition_log()
        if os.path.exists(d_path):
            with open(d_path, 'r') as f:
                # the csv will be only one line
                data = next(csv.reader(f))
                self.day_values = list(map(int, data))
        else:
            pass
        if os.path.exists(w_path):
            with open(w_path, 'r') as f:
                data = next(csv.reader(f))
                self.week_values = list(map(int, data))
        else:
            pass
        self.set_labels(labels_col1, 0)
        self.set_labels(labels_col2, 2)

    def init_ui(self) -> None:
        self.setShowGrid(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().hide()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QTableView.NoSelection)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def set_labels(self, labels: list, col: int) -> None:
        if col == 0:
            offset = -1
        elif col == 2:
            offset = 3
        else:
            offset = 0
        for row in range(1, 5):
            self.setItem(row, col, QTableWidgetItem(labels[row - 1]))
            self.setItem(row, col + 1, QTableWidgetItem(str(self.day_values[row + offset])))
        if col == 0:
            offset = -6
        elif col == 2:
            offset = -2
        else:
            offset = 0
        for row in range(6, 10):
            self.setItem(row, col, QTableWidgetItem(labels[row - 6]))
            self.setItem(row, col + 1, QTableWidgetItem(str(self.week_values[row + offset])))

    # ================================
    # Data
    # ================================

    def update_val(self, row: int, col: int, data: int) -> None:
        old_val = self.item(row, col).data(Qt.DisplayRole)
        new_val = int(old_val) + data
        self.setItem(row, col, QTableWidgetItem(str(new_val)))

    def update_day_val(self, row: int, col: int, data: int):
        self.update_val(row, col, data)
        if col == 1:
            self.day_values[row - 1] += data
        elif col == 3:
            self.day_values[row + 3] += data
        else:
            self.logger.debug('unexpected case at update_day_val')

    def update_week_val(self, row: int, col: int, data: int):
        self.update_val(row, col, data)
        if col == 1:
            self.week_values[row - 6] += data
        elif col == 3:
            self.week_values[row - 2] += data
        else:
            self.logger.debug('unexpected case at update_week_val')

    def on_newAward(self, data: dict) -> None:
        # 2: fuel, 3: ammo, 4: steel, 9: bauxite, 141: instant_build, 241: bp_build, 541, instant_repair, 741: bp_equip
        w_path, d_path = get_expedition_log()
        for key in data:
            if key == "2":
                self.update_day_val(1, 1, data[key])
                self.update_week_val(6, 1, data[key])
            elif key == "3":
                self.update_day_val(2, 1, data[key])
                self.update_week_val(7, 1, data[key])
            elif key == "4":
                self.update_day_val(3, 1, data[key])
                self.update_week_val(8, 1, data[key])
            elif key == "9":
                self.update_day_val(4, 1, data[key])
                self.update_week_val(9, 1, data[key])
            elif key == "541":
                self.update_day_val(1, 3, data[key])
                self.update_week_val(6, 3, data[key])
            elif key == "141":
                self.update_day_val(2, 3, data[key])
                self.update_week_val(7, 3, data[key])
            elif key == "241":
                self.update_day_val(3, 3, data[key])
                self.update_week_val(8, 3, data[key])
            elif key == "741":
                self.update_day_val(4, 3, data[key])
                self.update_week_val(9, 3, data[key])
            else:
                # 6, not in shipItem
                debug_str = f'unprocessed newAward key: {key}: {data[key]}'
                self.logger.debug(debug_str)
        with open(d_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.day_values)
        with open(w_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.week_values)

# End of File
