from PyQt5 import QtCore, QtGui, QtWidgets


class AlignListView(QtWidgets.QTreeView):
    '''
    Custom View for aligning left and right items
    '''
    def __init__(self, *args, **kwargs):
        # PUT keyword argument between *args and **kwargs!!
        # e.g. __init__(self, *args, rows=None, **kwargs)
        # TODO: styling?? the font is TOO small
        super(AlignListView, self).__init__()
        self.setModel(QtGui.QStandardItemModel(self))
        self.model().setColumnCount(2)
        self.setRootIsDecorated(False)
        self.setAllColumnsShowFocus(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setHeaderHidden(True)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def add_item(self, key, value, desc=None):
        # TODO: add function, when user clicked, pop up build/dev/repair etc
        first = QtGui.QStandardItem(key)
        first.setEditable(False)
        if desc != None:
            first.setToolTip(desc)
        else:
            pass
        second = QtGui.QStandardItem(value)
        second.setEditable(False)
        second.setTextAlignment(QtCore.Qt.AlignRight)
        self.model().appendRow([first, second])
        # index = self.model().rowCount()
        # return index, first, second
        return first, second

    def update_item(self, row, col, val):
        self.model().item(row, col).setText(str(val))


# End of File