from typing import Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QHeaderView


class AlignListView(QTreeView):
    """
    Custom View for aligning left and right items
    """

    def __init__(self):
        # PUT keyword argument between *args and **kwargs!!
        # e.g. __init__(self, *args, rows=None, **kwargs)
        # TODO: styling?? the font is TOO small
        super().__init__()
        self.setModel(QStandardItemModel(self))
        self.model().setColumnCount(2)
        self.setRootIsDecorated(False)
        self.setHeaderHidden(True)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.doubleClicked.connect(self.on_click)

    def on_click(self, index: int) -> None:
        pass

    def add_item(self, key: str, value: str, desc: str = None, is_limited: bool = False) -> Tuple[QStandardItem, QStandardItem]:
        # TODO: add function, when user clicked, pop up build/dev/repair etc
        first = QStandardItem(key)
        if desc is not None:
            first.setToolTip(desc)
        else:
            pass
        if is_limited:
            first.setForeground(QColor(255, 51, 51))
        else:
            pass
        second = QStandardItem(value)
        second.setTextAlignment(Qt.AlignRight)
        self.model().appendRow([first, second])
        # index = self.model().rowCount()
        # return index, first, second
        return first, second

    def update_item(self, row, col, val):
        self.model().item(row, col).setText(str(val))


class BathListView(AlignListView):
    def __init__(self):
        super().__init__()

    def on_click(self, index):
        pass
        # boat/repair/{ship cid}/{slot}
        # boat/rubdown/{ship cid}


class BuildListView(AlignListView):
    def __init__(self):
        super().__init__()

    def on_click(self, index):
        pass
        # dock/buildBoat/{slot}/{fuel}/{ammo}/{steel}/{baux}
        # dock/getBoat/{slot}
        # TODO: build 10 boats
        # TODO: cancel build


class DevListView(AlignListView):
    def __init__(self):
        super().__init__()

    def on_click(self, index):
        pass
        # dock/buildEquipment/{slot}/{fuel}/{ammo}/{steel}/{baux}
        # dock/dismantleEquipment       # I'm surprised, how do we know which to dismantle?
        # dock/getEquipment/2/
        # TODO: build 10 equips
        # TODO: cancel dev


class ExpListView(AlignListView):
    def __init__(self):
        super().__init__()

    def on_click(self, index):
        # print('exp')
        pass
        # explore/getResult/{exp_map}
        # explore/Start/{fleet}/{exp_map}
        # TODO: cancel exp


class TaskListView(AlignListView):
    def __init__(self):
        super().__init__()

    def on_click(self, index):
        pass
        # task/getAward/{task_cid}

# End of File
