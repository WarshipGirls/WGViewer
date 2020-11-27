import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHeaderView, QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea

import csv
from PyQt5 import QtCore, QtGui, QtWidgets


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class TabExpedition(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        csv_path = get_data_path('src/assets/data/exp_data.csv')

        self.table = ExpTable(self, csv_path)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)


class ExpTable(QtWidgets.QWidget):
    def __init__(self, parent, fileName):
        super(ExpTable, self).__init__(parent)
        self.fileName = fileName

        self.table_model = QtGui.QStandardItemModel(self)
        self.table_model.setColumnCount(15)
        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.load_csv(self.fileName)

        # self.table_view.setShowGrid(False)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().hide()
        self.table_view.verticalHeader().hide()
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for i in range(self.table_model.rowCount()):
            # HARDCODING
            self.table_view.setRowHeight(i, 20)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.table_view)

        self.highlight_data([3,4,5,6], highlight=False, bold=True)
        self.highlight_data([7,8,9,10], highlight=True, bold=True)

    def highlight_data(self, cols, highlight=False, bold=False):
        idxs = []
        for col in cols:
            idxs += self.get_n_max_val_idx_by_col(col)
        for i in idxs:
            item = self.table_model.itemFromIndex(i)
            if highlight == True:
                item.setBackground(QColor(213,255,204))
                item.setForeground(QColor('black'))
            else:
                pass
            if bold == True:
                f = item.font()
                f.setBold(True)
                item.setFont(f)
            else:
                pass

    def get_n_max_val_idx_by_col(self, col, n=4):
        tmp = {}
        for row in range(2, self.table_model.rowCount()):
            idx = self.table_model.index(row, col)
            d = idx.data()
            if d == "":
                continue
            else:
                if int(d) in tmp:
                    pass
                else:
                    tmp[int(d)] = []
                tmp[int(d)].append(idx)
        tmp_sorted = sorted(tmp, reverse=True)
        l = count = 0
        r = 1
        res = []
        while r != len(tmp_sorted):
            if tmp_sorted[l] != tmp_sorted[r]:
                count += 1
            else:
                pass
            l += 1
            r += 1
            res += tmp[tmp_sorted[l]]
            if count != n:
                pass
            else:
                break
        return res

    def load_csv(self, csv_path):
        with open(csv_path, "r") as f:
            for row in csv.reader(f): 
                items = [QtGui.QStandardItem(field) for field in row]
                self.table_model.appendRow(items)


# End of File