import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # DEBUG: confirmed SCROLL doesn't affect
        # scroll_box = QVBoxLayout()
        # scroll = QScrollArea()
        # scroll_box.addWidget(scroll)
        # scroll.setWidgetResizable(True)

        # content_widget = QWidget(scroll)
        # content_widget = QWidget()
        # content_layout = QVBoxLayout(content_widget)
        # content_widget.setLayout(content_layout)
        # scroll.setWidget(content_widget)

        # DEBUG: confirmed up/lo content widgets doesn't affect
        # lo = QWidget(content_widget)
        lo = QWidget()
        # content_layout.addWidget(lo)

        # DEBUG: confirmed QGridLayout doesn't affect
        # lo_layout = QGridLayout(lo)
        lo_layout = QVBoxLayout(lo)
        # lo_line_1 = QLabel("THIS IS LOW cell 1")
        # lo_layout.addWidget(lo_line_1, 0, 0, 1, 1)

        # tab = QTableView(lo)
        tab = QTableView()
        # sti = QStandardItemModel(lo)
        sti = QStandardItemModel()
        sti.appendRow([QStandardItem(str(i)) for i in range(5)])
        sti.insertRow(sti.rowCount())
        tab.setIndexWidget(sti.index(0, 0), QPushButton("fuck"))
        sti.setItem(1, 0, QStandardItem("???"))
        sti.setItem(1, 2, QStandardItem("???"))
        tab.setIndexWidget(sti.index(1, 1), QPushButton("fuck"))
        tab.setIndexWidget(sti.index(1, 2), QPushButton("fuck"))
        sti.appendRow([QStandardItem(str(i)) for i in range(5)])
        tab.setIndexWidget(sti.index(2, 1), QPushButton("fuck"))
        tab.setModel(sti)

        # lo_layout.addWidget(tab, 1, 0, 1, 6)
        lo_layout.addWidget(tab)

        # widget = QWidget()
        # widget.setLayout(scroll_box)
        # self.setCentralWidget(widget)
        # self.setCentralWidget(widget)

        # self.setCentralWidget(content_widget)
        
        # self.setCentralWidget(lo)

        self.setCentralWidget(tab)


app = QApplication(sys.argv)
# app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
window = MainWindow()
window.resize(1000, 600)
window.show() # IMPORTANT!!!!! Windows are hidden by default.
app.exec_()