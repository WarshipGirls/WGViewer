from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QHeaderView


class AlignListView(QTreeView):
    '''
    Custom View for aligning left and right items
    '''
    def __init__(self, *args, **kwargs):
        # PUT keyword argument between *args and **kwargs!!
        # e.g. __init__(self, *args, rows=None, **kwargs)
        # TODO: styling?? the font is TOO small
        super(AlignListView, self).__init__()
        self.setModel(QStandardItemModel(self))
        self.model().setColumnCount(2)
        self.setRootIsDecorated(False)
        self.setHeaderHidden(True)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)    # TODO: need to allow click event

        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def add_item(self, key, value, desc=None, is_limited=False):
        # TODO: add function, when user clicked, pop up build/dev/repair etc
        first = QStandardItem(key)
        if desc != None:
            first.setToolTip(desc)
        else:
            pass
        if is_limited != False:
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


# End of File