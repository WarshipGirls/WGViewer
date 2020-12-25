from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout,
    QTableView, QHeaderView, QAbstractScrollArea, QComboBox, QButtonGroup, QMainWindow, QLabel
)

from src import utils as wgv_utils
from src.data import get_processed_userShipVo


class PopupFleets(QMainWindow):
    def __init__(self, fleet_id: str):
        super().__init__()
        self.fleet = wgv_utils.get_exp_fleets()[fleet_id]
        self.user_ships = get_processed_userShipVo()

        self.setStyleSheet(wgv_utils.get_color_scheme())
        self.setWindowTitle('WGViewer - Expedition Fleet Selection')
        self.width = 200
        self.height = 500
        self.resize(self.width, self.height)

        self.curr_tab = QTableWidget()
        self.next_buttons = QButtonGroup()
        self.set_curr_table(0)

        content_layout_widget = QWidget(self)
        content_layout = QVBoxLayout(content_layout_widget)
        content_layout.addWidget(QLabel(f'Current Fleet {fleet_id}'))
        content_layout.addWidget(self.curr_tab)
        content_layout.addWidget(QLabel(f'Expedition Fleet for Next Map'))
        for b in self.next_buttons.buttons():
            content_layout.addWidget(b)
        self.setCentralWidget(content_layout_widget)

        self.show()

    def set_curr_table(self, row: int) -> None:
        self.curr_tab.setRowCount(6)
        self.curr_tab.setColumnCount(3)
        for ship_id in self.fleet:
            info = self.user_ships[str(ship_id)]
            self.curr_tab.setItem(row, 0, QTableWidgetItem(info['Class']))
            self.curr_tab.setItem(row, 1, QTableWidgetItem(info['Lv.']))
            self.curr_tab.setItem(row, 2, QTableWidgetItem(info['Name']))
            row += 1
        self.curr_tab.resizeColumnsToContents()
        self.curr_tab.resizeRowsToContents()
        self.curr_tab.setShowGrid(False)
        self.curr_tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.curr_tab.horizontalHeader().hide()
        self.curr_tab.verticalHeader().hide()
        self.curr_tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.curr_tab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.curr_tab.setEditTriggers(QTableView.NoEditTriggers)
        self.curr_tab.setFocusPolicy(Qt.NoFocus)
        self.curr_tab.setSelectionMode(QTableView.NoSelection)
        self.curr_tab.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def set_next_table(self) -> None:
        # TODO: like ship_window.py
        pass


class CustomComboBox(QComboBox):
    """
    QComboBox that can enable/disable certain items.
        Rendering dropdown items upon clicking
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.maps = wgv_utils.get_exp_list()
        self.addItems(self.maps)
        self.installEventFilter(self)

    def eventFilter(self, target, event):
        if target == self and event.type() == QEvent.MouseButtonPress:
            self.disable_maps()
        return False

    def disable_maps(self):
        for i in range(self.count()):
            item = self.model().item(i)
            item.setEnabled(item.text() not in self.parent.next_exp_maps)

# End of File
