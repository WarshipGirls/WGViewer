from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QTableView, QHeaderView, QAbstractScrollArea
)


class DailySummary(QTableWidget):
    def __init__(self):
        super().__init__()
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
        for row in range(6, 10):
            self.setItem(row, col, QTableWidgetItem(labels[row - 6]))

    def update_val(self, data: int, row: int, col: int) -> None:
        self.setItem(row, col, QTableWidgetItem(str(data)))

# End of File
