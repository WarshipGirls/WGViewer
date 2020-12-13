from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout

from src.gui.side_dock.dock import SideDock


class TabAdvanceFunctions(QWidget):
    sig_fuel = pyqtSignal(int)

    def __init__(self, tab_name: str, side_dock: SideDock):
        super().__init__()
        self.setObjectName(tab_name)

        test_btn = QPushButton('change to 10')
        test_btn.clicked.connect(self.update_fuel)

        test_btn2 = QPushButton('change to 9999999')
        test_btn2.clicked.connect(self.update_fuel2)

        self.sig_fuel.connect(side_dock.table_model.update_fuel)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(test_btn)
        self.layout.addWidget(test_btn2)
        self.setLayout(self.layout)

    def update_fuel(self) -> None:
        self.sig_fuel.emit(10)

    def update_fuel2(self) -> None:
        self.sig_fuel.emit(9999999)


# End of File
