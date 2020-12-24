from logging import Logger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QTableView, QHeaderView, QAbstractScrollArea
)


class DailySummary(QTableWidget):
    # TODO: refresh every day at local 0000
    # TODO: refresh every week at local 0000 Monday
    #   use a structure like user/week1/day1.txt
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

        self.init_table()
        self.init_ui()

    def init_table(self) -> None:
        self.setColumnCount(4)
        self.setRowCount(10)

        self.setItem(0, 0, QTableWidgetItem("DAILY SUMMARY"))
        self.setItem(5, 0, QTableWidgetItem("WEEKLY SUMMARY"))
        self.setSpan(0, 0, 1, 4)
        self.setSpan(5, 0, 1, 4)

        labels_col1 = ["Fuel", "Ammo.", "Steel", "Bauxite"]
        labels_col2 = ["Inst. Repair", "Inst. Build.", "Ship Blueprint", "Equip. Blueprint"]
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
        for row in range(1, 5):
            self.setItem(row, col, QTableWidgetItem(labels[row - 1]))
            self.setItem(row, col+1, QTableWidgetItem("0"))
        for row in range(6, 10):
            self.setItem(row, col, QTableWidgetItem(labels[row - 6]))
            self.setItem(row, col+1, QTableWidgetItem("0"))

    def update_val(self, row: int, col: int, data: int) -> None:
        old_val = self.item(row, col).data(Qt.DisplayRole)
        new_val = int(old_val) + data
        self.setItem(row, col, QTableWidgetItem(str(new_val)))

    def on_newAward(self, data: dict) -> None:
        # 2: fuel, 3: ammo, 4: steel, 9: bauxite, 141: instant_build, 241: bp_build, 541, instant_repair, 741: bp_equip
        for key in data:
            if key == "2":
                self.update_val(1, 1, data[key])
                self.update_val(6, 1, data[key])
            elif key == "3":
                self.update_val(2, 1, data[key])
                self.update_val(7, 1, data[key])
            elif key == "4":
                self.update_val(3, 1, data[key])
                self.update_val(8, 1, data[key])
            elif key == "9":
                self.update_val(4, 1, data[key])
                self.update_val(9, 1, data[key])
            elif key == "541":
                self.update_val(1, 3, data[key])
                self.update_val(6, 3, data[key])
            elif key == "141":
                self.update_val(2, 3, data[key])
                self.update_val(7, 3, data[key])
            elif key == "241":
                self.update_val(3, 3, data[key])
                self.update_val(8, 3, data[key])
            elif key == "741":
                self.update_val(4, 3, data[key])
                self.update_val(9, 3, data[key])
            else:
                self.logger.debug('unprocessed newAward')

# End of File
