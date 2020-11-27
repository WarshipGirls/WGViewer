from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QGridLayout

class DailySummary(QWidget):
    def __init__(self, cols_lim):
        super().__init__()
        self.cols_lim = cols_lim

        self.main_layout = QGridLayout(self)
        for i in range(5):
            for j in range(10):
                self.main_layout.addWidget(QLabel(str([i,j])), i, j)

        header = QLabel("DAILY SUMMARY")
        self.main_layout.addWidget(QLabel("DAILY SUMMARY"), 0, 0, 1, 4)
        self.main_layout.addWidget(QLabel("WEEKLY SUMMARY"), 0, 4, 1, 4)

        labels_col1 = ["Fuel","Ammo.","Steel","Bauxite"]
        labels_col2 = ["Inst. Repair","Inst. Build.","Ship Blueprint","Equip. Blueprint"]

        self.set_labels(labels_col1, 0)
        self.set_labels(labels_col2, 2)
        self.set_labels(labels_col1, 4)
        self.set_labels(labels_col2, 6)

        self.update_val(0, 1, 0)

    def set_labels(self, labels, col):
        for row in range(1, 5):
            self.main_layout.addWidget(QLabel(labels[row-1]), row, col, 1, 1)

    def update_val(self, data, row, col):
        item = self.main_layout.itemAtPosition(row, col).widget()
        print(item)
        # print(item.data())
        print(item.text())


# End of File