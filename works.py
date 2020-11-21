import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EquipsArray(QWidget):
    # def __init__(self, parent, equips_array):
    def __init__(self):
        super().__init__()

        try:
            # add your buttons
            layout = QHBoxLayout(self)
            print("FUCK MFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
            layout.addWidget(QPushButton('fuck'))
            layout.addWidget(QPushButton('fuck'))
            # layout.addWidget(QPushButton('fuck'))
            # layout.addWidget(QPushButton('fuck'))
            self.setLayout(layout)
        except Exception as e:
            logging.error(traceback.format_exc())
            # Logs the error appropriately. 


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    tab = QTableView()
    sti = QStandardItemModel()
    sti.appendRow([QStandardItem(str(i)) for i in range(5)])
    sti.appendRow([QStandardItem(str(i)) for i in range(3)])    # preset QStandardItem or not doesn't affect
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    # sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    sti.appendRow([])   # empty appendrow doesn't affect
    sti.insertRow(sti.rowCount())   # insertrow also works
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    tab.setModel(sti)
    # tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # tab.setIndexWidget(sti.index(0, 3), QPushButton("button"))
    tab.setIndexWidget(sti.index(0, 3), EquipsArray())
    tab.setIndexWidget(sti.index(1, 3), EquipsArray())
    tab.setIndexWidget(sti.index(2, 3), EquipsArray())
    tab.setIndexWidget(sti.index(3, 4), EquipsArray())
    tab.setIndexWidget(sti.index(4, 3), EquipsArray())

    idx = sti.index(5, 2)
    print(idx)
    tab.setIndexWidget(idx, EquipsArray())

    sti.setItem(6, 2, QStandardItem("WHYYYYY"))

    tab.show()
    tab.resize(800, 600)
    sys.exit(app.exec_())