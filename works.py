import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EquipsArray(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.addWidget(QPushButton('btn1'))
        layout.addWidget(QPushButton('btn2'))
        self.setLayout(layout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    tab = QTableView()
    sti = QStandardItemModel()
    tab.setModel(sti)
    sti.appendRow([QStandardItem(str(i)) for i in range(5)])
    sti.appendRow([QStandardItem(str(i)) for i in range(3)])    # preset QStandardItem or not doesn't affect
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    sti.appendRow([])   # empty appendrow doesn't affect
    sti.insertRow(sti.rowCount())   # insertrow also works
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    # tab.setIndexWidget(sti.index(0, 3), QPushButton("button"))
    tab.setIndexWidget(sti.index(0, 3), EquipsArray())
    tab.setIndexWidget(sti.index(1, 3), EquipsArray())
    tab.setIndexWidget(sti.index(2, 3), EquipsArray())
    tab.setIndexWidget(sti.index(3, 4), EquipsArray())
    tab.setIndexWidget(sti.index(4, 3), EquipsArray())
    sti.setItem(1, 0, QStandardItem("???"))
    sti.setItem(1, 2, QStandardItem("???"))

    idx = sti.index(5, 2)
    tab.setIndexWidget(idx, EquipsArray())

    tab.show()
    tab.resize(800, 600)
    sys.exit(app.exec_())