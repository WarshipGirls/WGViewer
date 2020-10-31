from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import traceback

class MyTable(QTableWidget):
    def __init__(self, rows):
        super().__init__()

        self.headers = ["", "Name", "ID", "Class", "Lv.", "HP", "Torp.", "Eva.", "Range", "ASW", "AA", "Fire.", "Armor", "Luck", "LOS", "Speed", "Slot", "Equip.", "Tact."]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setShowGrid(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        try:
            for i in range(rows):
                self.insertRow(i)
                # QPixmap vs. QImage https://stackoverflow.com/a/10315773
                path = "src/assets/S/S_NORMAL_1.png"    # wxh=363x88, cropped=156x88
                img = QPixmap()
                is_loaded = img.load(path)
                if is_loaded:
                    self.setRowHeight(i, 50)
                    self.setColumnWidth(i, 80)
                    thumbnail = QTableWidgetItem()
                    thumbnail.setData(Qt.DecorationRole, img.scaled(78, 44))
                    self.setItem(i, 0, thumbnail)
                else:
                    print(path)

            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setMaximumSize(self.getQTableWidgetSize())
            self.setMinimumSize(self.getQTableWidgetSize())
            self.show()
        except Exception as e:
            print(traceback.format_exc())

    def getQTableWidgetSize(self):
        w = self.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.columnCount()):
            w += self.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.horizontalHeader().height() + 4
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        return QSize(w, h)

class TopCheckboxes(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        for i in range(10):
            self.layout.setColumnStretch(i, 1)
        self.init_dropdowns()
        self.init_ship_boxes()
        self.resize(200,200)

    def init_dropdowns(self):
        lock_select = ["ALL", "YES", "NO"]
        self.add_dropdown("LOCK", lock_select, self.lock_handler, 0, 0)
        level_select = ["ALL", "Lv. 1", "> Lv. 1", "\u2265 Lv. 90", "\u2265 Lv. 100", "= Lv. 110"]
        self.add_dropdown("LEVEL", level_select, self.level_handler, 0, 1)
        value_select = ["Equip. Incl.", "Raw Value"]
        self.add_dropdown("VALUE", value_select, self.value_handler, 0, 2)
        mod_select = ["ALL", "Non-mod. Only", "Mod I. Only"]
        self.add_dropdown("MOD.", mod_select, self.mod_handler, 0, 3)
        rarity_select = ["\u2606 1", "\u2606 2", "\u2606 3", "\u2606 4", "\u2606 5", "\u2606 6"]
        self.add_dropdown("RARITY", rarity_select, self.rarity_handler, 0, 4)
        # current = 30/60
        # max only = 60
        health_select = ["Current Value", "Max Only"]
        self.add_dropdown("HEALTH", health_select, self.health_handler, 0, 5)
        married_select = ["ALL", "Married Only", "Non Married Only"]
        self.add_dropdown("MARRY", married_select, self.marry_handler, 0, 6)

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
        self.layout.addWidget(w, x, y, 1, 1)

    def lock_handler(self, text):
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
            self.layout.addWidget(b, 1, k, 1, 1)
            # https://stackoverflow.com/a/35821092
            self.first_boxes[k].stateChanged.connect(lambda _, b=self.first_boxes[k]: self.checkbox_handler(b))
        self.second_boxes = []
        for k, v in enumerate(second_row_types):
            b = QCheckBox(v, self)
            self.second_boxes.append(b)
            self.layout.addWidget(b, 2, k, 1, 1)
            self.second_boxes[k].stateChanged.connect(lambda _, b=self.second_boxes[k]: self.checkbox_handler(b))

    def checkbox_handler(self, cb):
        if cb.isChecked():
            print("checked " + cb.text())
        else:
            print("unchecked " + cb.text())

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        list_box = QVBoxLayout(self)
        self.setLayout(list_box)

        scroll = QScrollArea(self)
        list_box.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)

        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)
        # x = MyTable(50)
        # y = MyTable(50)
        ck = TopCheckboxes()
        scroll_layout.addWidget(ck)
        # scroll_layout.addWidget(x)
        # scroll_layout.addWidget(y)
        scroll.setWidget(scroll_content)
        self.show()


# App = QApplication(sys.argv)
# win = MyWindow()
# sys.exit(App.exec())

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        # label1 = QLabel("Widget in Tab 1.")
        win = MyWindow()
        # qss_path = 'src/assets/dark_style.qss'
        # qss_file = open(qss_path).read()
        # self.setStyleSheet(qss_file)
        # import qdarkstyle
        # self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        label2 = QLabel("Widget in Tab 2.")
        tabwidget = QTabWidget()
        tabwidget.addTab(win, "Tab 1")
        tabwidget.addTab(label2, "Tab 2")
        layout.addWidget(tabwidget, 0, 0)

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())