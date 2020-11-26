from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal

from . import constant as SCONST


class TopCheckboxes(QWidget):
    sig_value_select = pyqtSignal(str)

    def __init__(self, parent, model, proxy):
        super().__init__()
        self.layout = QGridLayout(parent)
        self.model = model
        self.proxy = proxy

        for i in range(10):
            self.layout.setColumnStretch(i, 1)
        self.init_dropdowns()
        self.init_ship_boxes()
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)

        self.sig_value_select.connect(self.model.on_stats_changed)

    def init_dropdowns(self):
        self.add_dropdown("LOCK", SCONST.lock_select, self.proxy.setLockFilter, 0, 0)
        self.add_dropdown("LEVEL", SCONST.level_select, self.proxy.setLevelFilter, 0, 1)
        # current = 30/60, max only = 60
        self.add_dropdown("VALUE", SCONST.value_select, self.value_handler, 0, 2)
        self.add_dropdown("MOD.", SCONST.mod_select, self.proxy.setModFilter, 0, 3)
        self.add_dropdown("Type/Size", SCONST.type_size_select, self.proxy.setTypeSizeFilter, 0, 4)
        self.add_dropdown("RARITY", SCONST.rarity_select, self.proxy.setRarityFilter, 0, 5)
        self.add_dropdown("MARRY", SCONST.married_select, self.proxy.setMarryFilter, 0, 7)

    def add_dropdown(self, label, choices, handler, x, y):
        w = QWidget()
        wl = QHBoxLayout()
        w.setLayout(wl)
        l = QLabel(label)
        lc = QComboBox()
        lc.addItems(choices)
        lc.currentTextChanged.connect(handler)
        wl.addWidget(l)
        wl.addWidget(lc)
        wl.setStretch(0, 2)
        wl.setStretch(1, 8)
        self.layout.addWidget(w, x, y)

    def value_handler(self, text):
        self.sig_value_select.emit(text)

    def init_ship_boxes(self):
        # in the ascending order of ship types (int)
        first_row_types = ["CV", "CVL", "AV", "BB", "BBV", "BC", "CA", "CAV", "CLT", "CL"]
        second_row_types = ["BM", "DD", "SSV", "SS", "SC", "AP", "ASDG", "AADG", "CB", "BBG"]

        self.first_boxes = []
        for k, v in enumerate(first_row_types):
            b = QCheckBox(v, self)
            self.first_boxes.append(b)
            # self.layout.addWidget(b, 1, k, 1, 1)
            self.layout.addWidget(b, 1, k)
            # https://stackoverflow.com/a/35821092
            self.first_boxes[k].stateChanged.connect(lambda _, b=self.first_boxes[k]: self.checkbox_handler(b))
        self.second_boxes = []
        for k, v in enumerate(second_row_types):
            b = QCheckBox(v, self)
            self.second_boxes.append(b)
            # self.layout.addWidget(b, 2, k, 1, 1)
            self.layout.addWidget(b, 2, k)
            self.second_boxes[k].stateChanged.connect(lambda _, b=self.second_boxes[k]: self.checkbox_handler(b))

    def checkbox_handler(self, cb):
        # TODO
        if cb.isChecked():
            print("checked " + cb.text())
        else:
            print("unchecked " + cb.text())


# End of File