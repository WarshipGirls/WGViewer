import sys
import logging
import qdarkstyle
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


# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)


#     scroll_box = QVBoxLayout()

#     app.setCentralWidget


#     tab = QTableView()
#     sti = QStandardItemModel()
#     sti.appendRow([QStandardItem(str(i)) for i in range(5)])
#     sti.appendRow([QStandardItem(str(i)) for i in range(3)])    # preset QStandardItem or not doesn't affect
#     sti.appendRow([QStandardItem(str(i)) for i in range(4)])
#     sti.appendRow([QStandardItem(str(i)) for i in range(4)])
#     # sti.appendRow([QStandardItem(str(i)) for i in range(4)])
#     sti.appendRow([])   # empty appendrow doesn't affect
#     sti.insertRow(sti.rowCount())   # insertrow also works
#     sti.appendRow([QStandardItem(str(i)) for i in range(4)])
#     tab.setModel(sti)
#     # tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
#     # tab.setIndexWidget(sti.index(0, 3), QPushButton("button"))
#     tab.setIndexWidget(sti.index(0, 3), EquipsArray())
#     tab.setIndexWidget(sti.index(1, 3), EquipsArray())
#     tab.setIndexWidget(sti.index(2, 3), EquipsArray())
#     tab.setIndexWidget(sti.index(3, 4), EquipsArray())
#     tab.setIndexWidget(sti.index(4, 3), EquipsArray())

#     idx = sti.index(5, 2)
#     print(idx)
#     tab.setIndexWidget(idx, EquipsArray())

#     sti.setItem(6, 2, QStandardItem("WHYYYYY"))

#     # resize doesn't affect the buttons
#     header = tab.horizontalHeader()
#     for i in range(sti.columnCount()):
#         header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
#     # qdarkstyle doesn't affect
#     app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

#     tab.setShowGrid(False)

#     tab.show()
#     sys.exit(app.exec_())



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        scroll_box = QVBoxLayout()
        scroll = QScrollArea()
        scroll_box.addWidget(scroll)
        scroll.setWidgetResizable(True)

        content_widget = QWidget(scroll)
        content_layout = QVBoxLayout(content_widget)
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)

        # up = QWidget(content_widget)
        lo = QWidget(content_widget)

        # content_layout.addWidget(up)
        content_layout.addWidget(lo)

        # up_layout = QHBoxLayout(up)
        # up_line_1 = QLabel("uuuuuuuuuuuuuuuuuuuuuu")
        # up_layout.addWidget(up_line_1)

        lo_layout = QGridLayout(lo)
        lo_line_1 = QLabel("THIS IS LOW")
        lo_layout.addWidget(lo_line_1, 0, 0, 1, 1)

        tab = QTableView()
        sti = QStandardItemModel()
        sti.appendRow([QStandardItem(str(i)) for i in range(5)])
        sti.insertRow(sti.rowCount())
        # tab.setIndexWidget(sti.index(0, 0), QPushButton("fuck"))
        sti.setItem(1, 0, QStandardItem("???"))
        tab.setIndexWidget(sti.index(1, 1), QPushButton("fuck"))
        sti.appendRow([QStandardItem(str(i)) for i in range(5)])
        tab.setModel(sti)

        lo_layout.addWidget(tab, 1, 0, 1, 6)

        widget = QWidget()
        widget.setLayout(scroll_box)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
# app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
window = MainWindow()
window.show() # IMPORTANT!!!!! Windows are hidden by default.
app.exec_()