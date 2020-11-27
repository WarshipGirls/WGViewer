from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QCheckBox, QPushButton
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
        for i in range(22):
            self.layout.setColumnStretch(i, 1)

        self.init_button()
        self.init_dropdowns()
        self.init_ship_boxes()

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)

        self.sig_value_select.connect(self.model.on_stats_changed)

    def init_button(self):
        button = QPushButton("CLEAR\nALL\nFILTER\nCRETERIA")
        button.clicked.connect(self._clear_filters)
        self.layout.addWidget(button, 0, 0, 3, 1)
        self.layout.setColumnStretch(0, 0)

    def init_dropdowns(self):
        self.add_dropdown_on_index("COUNTRY", SCONST.country_select, self.proxy.setCountryFilter, 0, 1, 4)
        self.add_dropdown_on_index("RARITY", SCONST.rarity_select, self.proxy.setRarityFilter, 0, 5, 2)
        self.add_dropdown_on_text("TYPE", SCONST.type_size_select, self.proxy.setTypeSizeFilter, 0, 7, 2)
        self.add_dropdown_on_text("LEVEL", SCONST.level_select, self.proxy.setLevelFilter, 0, 9, 2)
        self.add_dropdown_on_text("LOCK", SCONST.lock_select, self.proxy.setLockFilter, 0, 11, 2)
        self.add_dropdown_on_text("MARRY", SCONST.married_select, self.proxy.setMarryFilter, 0, 13, 2)
        self.add_dropdown_on_text("MOD.", SCONST.mod_select, self.proxy.setModFilter, 0, 15, 2)
        # value populating is slow, takes extra step
        self.value_dropdown = self.add_dropdown_on_text("VALUE", SCONST.value_select, self.value_handler, 0, 17, 3)

    def init_ship_boxes(self):
        # in the ascending order of ship types (int)
        first_row_types = ["CV", "CVL", "AV", "BB", "BBV", "BC", "CA", "CAV", "CLT", "CL"]
        second_row_types = ["BM", "DD", "SSV", "SS", "SC", "AP", "ASDG", "AADG", "CB", "BBG"]

        self.first_boxes = []
        for k, v in enumerate(first_row_types):
            b = QCheckBox(v, self)
            self.first_boxes.append(b)
            self.layout.addWidget(b, 1, k*2+1, 1, 2)
            # https://stackoverflow.com/a/35821092
            self.first_boxes[k].stateChanged.connect(lambda _, b=self.first_boxes[k]: self.proxy.setCheckBoxFilter(b))
        self.second_boxes = []
        for k, v in enumerate(second_row_types):
            b = QCheckBox(v, self)
            self.second_boxes.append(b)
            self.layout.addWidget(b, 2, k*2+1, 1, 2)
            self.second_boxes[k].stateChanged.connect(lambda _, b=self.second_boxes[k]: self.proxy.setCheckBoxFilter(b))

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
        return lc

    def value_handler(self, text):
        # TODO https://github.com/WarshipGirls/WGViewer/issues/21
        self.sig_value_select.emit(text)

    def _clear_filters(self):
        self.proxy.setCountryFilter(None)
        self.proxy.setRarityFilter(None)
        self.proxy.setTypeSizeFilter(None)
        self.proxy.setLevelFilter(None)
        self.proxy.setLockFilter(None)
        self.proxy.setMarryFilter(None)
        self.proxy.setModFilter(None)

        if self.value_dropdown.currentText() == 'Curr. (w/ Equip.)':
            pass
        else:
            self.proxy.value_handler('Curr. (w/ Equip.)')

        for b in self.first_boxes:
            b.setChecked(False)
        for b in self.second_boxes:
            b.setChecked(False)
        self.proxy.setCheckBoxFilter(None)


# End of File