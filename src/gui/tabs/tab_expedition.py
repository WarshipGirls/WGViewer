import os
import sys

from PyQt5.QtWidgets import QWidget, QHeaderView
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

        # scroll_box = QVBoxLayout(self)
        # self.setLayout(scroll_box)
        # scroll = QScrollArea(self)
        # scroll_box.addWidget(scroll)
        # scroll.setWidgetResizable(True)

        # self.content_widget = QWidget(scroll)
        # self.content_layout = QVBoxLayout(self.content_widget)
        # self.content_layout.setContentsMargins(0,0,0,0)
        # self.content_widget.setLayout(self.content_layout)
        # scroll.setWidget(self.content_widget)

        # self.upper_content_widget = QWidget(self.content_widget)
        # self.lower_content_widget = QWidget(self.content_widget)

        # self.content_layout.addWidget(self.upper_content_widget)
        # self.content_layout.addWidget(self.lower_content_widget)
        # tmp = QtWidgets.QLabel('hhhhh', self.lower_content_widget)
        # self.content_layout.setStretch(0, 10)
        # self.content_layout.setStretch(1, 1)

        # self.exp_table_widget = MyWindow(self.upper_content_widget, csv_path)


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

        header = self.table_view.horizontalHeader()
        for i in range(self.table_model.columnCount()):
            # QHeaderView.Stretch
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.table_view)

        # self.table_view.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

    def load_csv(self, csv_path):
        with open(csv_path, "r") as f:
            for row in csv.reader(f): 
                items = [QtGui.QStandardItem(field) for field in row]
                self.table_model.appendRow(items)

    '''
    def writeCsv(self, fileName):
        with open(fileName, "w") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.table_model.rowCount()):
                fields = [
                    self.table_model.data(
                        self.table_model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.table_model.columnCount())
                ]
                writer.writerow(fields)
    '''


# End of File