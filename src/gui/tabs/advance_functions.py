from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QVBoxLayout

from src.gui.side_dock.dock import SideDock


class TabAdvanceFunctions(QWidget):
    sig_fuel = pyqtSignal(int)

    def __init__(self, tab_name: str, side_dock: SideDock):
        super().__init__()
        self.setObjectName(tab_name)

        # self.counter = 5
        # self.tr = QTimer()
        # self.tr.setInterval(1000)
        # self.tr.timeout.connect(self.count_down)

        t_label = QLabel("UNDER CONSTRUCTION. NOT AVAILABLE TO USER YET")
        # test_btn = QPushButton('change to 10')
        # test_btn.clicked.connect(self.update_fuel)
        #
        # test_btn2 = QPushButton('change to 9999999')
        # test_btn2.clicked.connect(self.update_fuel2)
        #
        # self.test_label = QLabel('????????????')
        #
        # self.sig_fuel.connect(side_dock.table_model.update_fuel)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(t_label)
        # self.layout.addWidget(test_btn)
        # self.layout.addWidget(test_btn2)
        # self.layout.addWidget(self.test_label)
        self.setLayout(self.layout)
        #
        # self.tr.start()

    # def count_down(self):
    #     print(locals())
    #     self.counter -= 1
    #     if self.counter >= 0:
    #         pass
    #     else:
    #         self.counter = 5
    #     self.test_label.setText(str(self.counter))
    #
    # def update_fuel(self) -> None:
    #     self.sig_fuel.emit(10)
    #
    # def update_fuel2(self) -> None:
    #     self.sig_fuel.emit(9999999)


# End of File
