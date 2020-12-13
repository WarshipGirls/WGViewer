from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem,
    QHBoxLayout,
    QTableView, QHeaderView, QAbstractScrollArea
)


class DailySummary(QWidget):
    def __init__(self):
        super().__init__()

        self.tab = QTableWidget()
        self.init_table()
        self.init_ui()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)

    def init_table(self) -> None:
        self.tab.setColumnCount(8)
        self.tab.setRowCount(5)

        self.tab.setItem(0, 0, QTableWidgetItem("DAILY SUMMARY"))
        self.tab.setItem(0, 4, QTableWidgetItem("WEEKLY SUMMARY"))
        self.tab.setSpan(0, 0, 1, 4)
        self.tab.setSpan(0, 4, 1, 4)

        labels_col1 = ["Fuel", "Ammo.", "Steel", "Bauxite"]
        labels_col2 = ["Inst. Repair", "Inst. Build.", "Ship Blueprint", "Equip. Blueprint"]
        self.set_labels(labels_col1, 0)
        self.set_labels(labels_col2, 2)
        self.set_labels(labels_col1, 4)
        self.set_labels(labels_col2, 6)

    def init_ui(self) -> None:
        self.tab.setShowGrid(False)
        self.tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.horizontalHeader().hide()
        self.tab.verticalHeader().hide()
        self.tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab.setEditTriggers(QTableView.NoEditTriggers)
        self.tab.setFocusPolicy(Qt.NoFocus)
        self.tab.setSelectionMode(QTableView.NoSelection)
        self.tab.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def set_labels(self, labels: list, col: int) -> None:
        for row in range(1, 5):
            self.tab.setItem(row, col, QTableWidgetItem(labels[row - 1]))

    def update_val(self, data: int, row: int, col: int) -> None:
        self.tab.setItem(row, col, QTableWidgetItem(str(data)))

# End of File
