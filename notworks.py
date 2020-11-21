import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        lo = QWidget()
        lo_layout = QVBoxLayout(lo)

        tab = QTableView()
        sti = QStandardItemModel()
        tab.setModel(sti)
        sti.appendRow([QStandardItem(str(i)) for i in range(5)])
        sti.insertRow(sti.rowCount())
        tab.setIndexWidget(sti.index(0, 0), QPushButton("fuck"))
        sti.setItem(1, 0, QStandardItem("???"))
        sti.setItem(1, 2, QStandardItem("???"))
        tab.setIndexWidget(sti.index(1, 1), QPushButton("fuck"))
        tab.setIndexWidget(sti.index(1, 2), QPushButton("fuck"))
        sti.appendRow([QStandardItem(str(i)) for i in range(5)])
        tab.setIndexWidget(sti.index(2, 1), QPushButton("fuck"))

        lo_layout.addWidget(tab)
        self.setCentralWidget(tab)


app = QApplication(sys.argv)
window = MainWindow()
window.resize(1000, 600)
window.show() # IMPORTANT!!!!! Windows are hidden by default.
app.exec_()