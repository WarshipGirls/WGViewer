from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QComboBox, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout


class TopCheckboxes(QWidget):
    def __init__(self, parent, proxy):
        super().__init__()
        self.layout = QGridLayout(parent)
        self.proxy = proxy
        # self.layout.setContentsMargins(0,0,0,0)
        # TODO: fix the size
        # self.setGeometry(0,0, 500, 100)
        # self.resize(200, 200)

        for i in range(10):
            self.layout.setColumnStretch(i, 1)
        self.init_dropdowns()
        self.init_ship_boxes()
        # self.layout.setRowMinimumHeight(0, 0)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)
        # self.setFixedHeight(100)
        # self.setFixedWidth(1000)  # not working as expected
        print(self.width(), self.height())

    def init_dropdowns(self):
        lock_select = ["ALL", "YES", "NO"]
        level_select = ["ALL", "Lv. 1", "> Lv. 1", "\u2265 Lv. 90", "\u2265 Lv. 100", "= Lv. 110"]
        value_select = ["Equip. Incl.", "Raw Value"]
        mod_select = ["ALL", "Non-mod. Only", "Mod I. Only"]
        health_select = ["Current Value", "Max Only"]
        rarity_select = ["\u2606 1", "\u2606 2", "\u2606 3", "\u2606 4", "\u2606 5", "\u2606 6"]
        married_select = ["ALL", "Married Only", "Non Married Only"]
        size_select = ["ALL", "SMALL", "MIDIUM", "LARGE"]
        # self.add_dropdown("LOCK", lock_select, self.lock_handler, 0, 0)
        self.add_dropdown("LOCK", lock_select, self.proxy.setLockFilter, 0, 0)
        self.add_dropdown("LEVEL", level_select, self.level_handler, 0, 1)
        self.add_dropdown("VALUE", value_select, self.value_handler, 0, 2)
        self.add_dropdown("MOD.", mod_select, self.mod_handler, 0, 3)
        self.add_dropdown("Type (Size)", size_select, self.size_handler, 0, 4)
        self.add_dropdown("RARITY", rarity_select, self.rarity_handler, 0, 5)
        # current = 30/60, max only = 60
        self.add_dropdown("HEALTH", health_select, self.health_handler, 0, 6)
        self.add_dropdown("MARRY", married_select, self.marry_handler, 0, 7)

    def add_dropdown(self, label, choices, handler, x, y):
        w = QWidget()
        # w.setFixedHeight(40)
        # w.setFixedWidth(200)  # not working as expected
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

    def lock_handler(self, text):
        print(text)

    def size_handler(self, text):
        print(text)

    def level_handler(self, text):
        print(text)

    def value_handler(self, text):
        print(text)

    def mod_handler(self, text):
        print(text)

    def rarity_handler(self, text):
        print(text)

    def health_handler(self, text):
        print(text)

    def marry_handler(self, text):
        print(text)

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
        if cb.isChecked():
            print("checked " + cb.text())
        else:
            print("unchecked " + cb.text())


# End of File