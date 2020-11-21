from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Buttons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.addWidget(QPushButton('btn1'))
        layout.addWidget(QPushButton('btn2'))
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        tab = QTableView()
        sti = QStandardItemModel()
        if True:    # This shows the buttons in a cell
            tab.setModel(sti)
        else:       # This does not show the buttons
            proxy = QSortFilterProxyModel()
            proxy.setSourceModel(sti)
            tab.setModel(proxy)
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(sti)
        tab.setModel(proxy)

        sti.appendRow([QStandardItem(str(i)) for i in range(5)])
        # tab.setIndexWidget(sti.index(0, 0), QPushButton("hi"))
        tab.setIndexWidget(tab.model().index(0, 0), QPushButton("hi"))
        sti.appendRow([])
        tab.setIndexWidget(tab.model().index(1, 2), Buttons())
        self.setCentralWidget(tab)

app = QApplication([])
window = MainWindow()
window.resize(800, 600)
window.show()
app.exec_()