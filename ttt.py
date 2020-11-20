import sys
import logging
import qdarkstyle
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class EquipsArray(QWidget):
    # def __init__(self, parent, equips_array):
    def __init__(self):
        super().__init__()

        try:
            # add your buttons
            layout = QHBoxLayout(self)
            print("FUCK MFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")

            # adjust spacings to your needs
            # layout.setContentsMargins(0,0,0,0)
            # layout.setSpacing(0)

            # prefix = "src/assets/E/equip_L_"
            # # equips = list(map(int, equips_array))
            # for e in equips_array:
            #     e = str(e)
            #     if e == '':
            #         continue
            #     else:
            #         pass
            #     try:
            #         img_path = prefix + str(int(e[3:6])) + ".png"
            #         img = QPixmap()
            #         is_loaded = img.load(get_data_path(img_path))
            #         if is_loaded:
            #             # i = QStandardItem()
            #             # i.setData(QVariant(img), Qt.DecorationRole)
            #             l = QLabel(self)
            #             l.setPixmap(img)
            #             layout.addWidget(l)
            #         else:
            #             print("NOT LOADDDDDDDD")
            #     except ValueError as e:
            #         print(e)

            layout.addWidget(QPushButton('fuck'))
            layout.addWidget(QPushButton('fuck'))
            # layout.addWidget(QPushButton('fuck'))
            # layout.addWidget(QPushButton('fuck'))

            self.setLayout(layout)
        except Exception as e:
            logging.error(traceback.format_exc())
            # Logs the error appropriately. 

def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # app.setStyle("fusion")
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

    # resize doesn't affect the buttons
    header = tab.horizontalHeader()
    for i in range(sti.columnCount()):
        header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
    # qdarkstyle doesn't affect
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    tab.setShowGrid(False)

    tab.show()
    sys.exit(app.exec_())