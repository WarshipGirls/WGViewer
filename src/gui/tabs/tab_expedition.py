import csv
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QTableView
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea

from ...data import data as wgr_data


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


class ExpTable(QWidget):
    # Long term TODO: max coeff. by iter thru user's engineering bay stats
    def __init__(self, parent, fileName):
        super(ExpTable, self).__init__(parent)
        self.fileName = fileName

        self.table_model = QStandardItemModel(self)
        self.table_model.setColumnCount(15)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.load_csv(self.fileName)

        # self.table_view.setShowGrid(False)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().hide()
        self.table_view.verticalHeader().hide()
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        # self.table_view.setSelectionMode(QTableWidget.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for i in range(self.table_model.rowCount()):
            # HARDCODING
            self.table_view.setRowHeight(i, 20)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.table_view)
        self.merge_cells()
        self.populate_expectation_income()

        self.highlight_data([3,4,5,6], highlight_color=None, bold=True)
        self.highlight_data([7,8,9,10], highlight_color=QColor(128, 159, 255), bold=True)
        self.highlight_data([11,12,13,14], highlight_color=QColor(0, 153, 51), bold=True)

    def merge_cells(self):
        self.table_view.setSpan(0,0,1,3)
        self.table_view.setSpan(0,3,1,4)
        self.table_view.setSpan(0,7,1,4)
        self.table_view.setSpan(0,11,1,2)

    def highlight_data(self, cols, highlight_color=None, bold=False):
        idxs = []
        maps = set()
        for col in cols:
            idxs += self.get_n_max_val_idx_by_col(col)
        for i in idxs:
            item = self.table_model.itemFromIndex(i)
            if isinstance(highlight_color, QColor):
                maps.add(item.row())
                item.setBackground(highlight_color)
                item.setForeground(QColor('black'))
            else:
                pass
            if bold == True:
                f = item.font()
                f.setBold(True)
                item.setFont(f)
            else:
                pass
        for m in maps:
            item = self.table_model.itemFromIndex(self.table_model.index(m, 0))
            item.setBackground(QColor(0, 153, 51))

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
            res += tmp[tmp_sorted[l]]
            l += 1
            r += 1
            if count != n:
                pass
            else:
                break
        return res

    def populate_expectation_income(self):
        rate = wgr_data.get_big_success_rate()
        for row in range(2, self.table_model.rowCount()):
            for col in [11,12,13,14]:
                d = self.table_model.index(row, col-4).data()
                if d == "":
                    continue
                else:
                    d = int(d)
                    t = (1-rate)*d + rate*d*1.5
                    self.table_model.setItem(row, col, QStandardItem(str(int(t))))

    def load_csv(self, csv_path):
        with open(csv_path, "r") as f:
            for row in csv.reader(f): 
                items = [QStandardItem(field) for field in row]
                self.table_model.appendRow(items)
        
        rate = str(wgr_data.get_big_success_rate())
        self.table_model.setItem(0, self.table_model.columnCount()-1, QStandardItem(rate))


# End of File