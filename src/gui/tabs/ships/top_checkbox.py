from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout

from . import constant as SCONST


class TopCheckboxes(QWidget):
    sig_value_select = pyqtSignal(str)

    def __init__(self, parent, model, proxy):
        super().__init__()
        self.layout = QGridLayout(parent)
        self.model = model
        self.proxy = proxy

        # HARDCODING
        for i in range(10):
            self.layout.setColumnStretch(i, 1)
        self.init_dropdowns()
        self.init_ship_boxes()
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)

        self.sig_value_select.connect(self.model.on_stats_changed)

    def init_dropdowns(self):
        self.add_dropdown_on_index("COUNTRY", SCONST.country_select, self.proxy.setCountryFilter, 0, 0, 2)
        self.add_dropdown_on_index("RARITY", SCONST.rarity_select, self.proxy.setRarityFilter, 0, 2)
        self.add_dropdown_on_text("TYPE", SCONST.type_size_select, self.proxy.setTypeSizeFilter, 0, 3)
        self.add_dropdown_on_text("LEVEL", SCONST.level_select, self.proxy.setLevelFilter, 0, 4)
        self.add_dropdown_on_text("LOCK", SCONST.lock_select, self.proxy.setLockFilter, 0, 5)
        # current = 30/60, max only = 60
        self.add_dropdown_on_text("MARRY", SCONST.married_select, self.proxy.setMarryFilter, 0, 6)
        self.add_dropdown_on_text("MOD.", SCONST.mod_select, self.proxy.setModFilter, 0, 7)
        self.add_dropdown_on_text("VALUE", SCONST.value_select, self.value_handler, 0, 8, 2)

    def _add_dropdown(self, label, combobox, x, y, y_span):
        w = QWidget()
        wl = QHBoxLayout()
        w.setLayout(wl)
        l = QLabel(label)
        wl.addWidget(l)
        wl.addWidget(combobox)
        wl.setStretch(0, 2)
        wl.setStretch(1, 8)
        self.layout.addWidget(w, x, y, 1, y_span)

    def add_dropdown_on_index(self, label, choices, handler, x, y, y_span=1):
        lc = QComboBox()
        lc.addItems(choices)
        lc.currentIndexChanged.connect(handler)
        lc.setFont(QFont('Consolas'))
        self._add_dropdown(label, lc, x, y, y_span)

    def add_dropdown_on_text(self, label, choices, handler, x, y, y_span=1):
        lc = QComboBox()
        lc.addItems(choices)
        lc.currentTextChanged.connect(handler)
        lc.setFont(QFont('Consolas'))
        self._add_dropdown(label, lc, x, y, y_span)

    def value_handler(self, text):
        # TODO https://github.com/WarshipGirls/WGViewer/issues/21
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
        # TODO TODO
        if cb.isChecked():
            print("checked " + cb.text())
        else:
            print("unchecked " + cb.text())


# End of File