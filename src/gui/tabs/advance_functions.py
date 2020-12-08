from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout

from src.gui.side_dock.dock import SideDock


class TabAdvanceFunctions(QWidget):
    def __init__(self, tab_name: str, side_dock: SideDock):
        super().__init__()
        self.setObjectName(tab_name)

        test_btn = QPushButton('test')
        test_btn.clicked.connect(side_dock.update_fuel)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(test_btn)
        self.setLayout(self.layout)


# End of File
